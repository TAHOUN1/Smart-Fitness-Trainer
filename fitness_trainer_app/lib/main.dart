import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'services/workout_service.dart';
import 'package:image_picker/image_picker.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Request camera permission first
  final status = await Permission.camera.request();
  if (!status.isGranted) {
    runApp(const MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('Camera permission is required to use this app'),
        ),
      ),
    ));
    return;
  }

  // Get available cameras
  final cameras = await availableCameras();
  if (cameras.isEmpty) {
    runApp(const MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('No cameras found on this device'),
        ),
      ),
    ));
    return;
  }

  runApp(MyApp(cameras: cameras));
}

class MyApp extends StatelessWidget {
  final List<CameraDescription> cameras;

  const MyApp({super.key, required this.cameras});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fitness Trainer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: CameraScreen(cameras: cameras),
    );
  }
}

class CameraScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const CameraScreen({super.key, required this.cameras});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  final WorkoutService _workoutService = WorkoutService();
  String _workoutStatus = 'No workout detected';
  bool _isProcessing = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      final camera = widget.cameras.first;
      _controller = CameraController(
        camera,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      
      _initializeControllerFuture = _controller!.initialize();
      await _initializeControllerFuture;
      
      if (mounted) {
        setState(() {});
      }
    } catch (e) {
      setState(() {
        _error = 'Failed to initialize camera: $e';
      });
    }
  }

  Future<void> _processFrame() async {
    if (_isProcessing || _controller == null) return;

    setState(() {
      _isProcessing = true;
    });

    try {
      final image = await _controller!.takePicture();
      final result = await _workoutService.processFrame(File(image.path));
      
      setState(() {
        _workoutStatus = result['workout_type'] ?? 'No workout detected';
      });
    } catch (e) {
      setState(() {
        _workoutStatus = 'Error: $e';
      });
    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  Future<void> _uploadVideo() async {
    final ImagePicker picker = ImagePicker();
    final XFile? video = await picker.pickVideo(source: ImageSource.gallery);

    if (video != null) {
      setState(() {
        _isProcessing = true;
      });

      try {
        final result = await _workoutService.processVideo(File(video.path));
        setState(() {
          _workoutStatus = result['workout_type'] ?? 'No workout detected';
        });
      } catch (e) {
        setState(() {
          _workoutStatus = 'Error: $e';
        });
      } finally {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Fitness Trainer')),
        body: Center(child: Text(_error!)),
      );
    }

    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Fitness Trainer'),
      ),
      body: Column(
        children: [
          Expanded(
            child: CameraPreview(_controller!),
          ),
          Container(
            padding: const EdgeInsets.all(16.0),
            color: Colors.black87,
            child: Column(
              children: [
                Text(
                  _workoutStatus,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                  ),
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: _isProcessing ? null : _processFrame,
                  child: Text(_isProcessing ? 'Processing...' : 'Detect Workout'),
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: _isProcessing ? null : _uploadVideo,
                  child: Text(_isProcessing ? 'Processing...' : 'Upload Video'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
