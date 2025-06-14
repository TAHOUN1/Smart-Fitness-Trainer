import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

class WorkoutService {
  static const String baseUrl = 'http://10.0.2.2:8000'; // For Android emulator
  // Use your computer's IP address when testing on a real device

  Future<Map<String, dynamic>> processVideo(File videoFile) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/process-video'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'video',
          videoFile.path,
        ),
      );

      var response = await request.send();
      var responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        return json.decode(responseData);
      } else {
        throw Exception('Failed to process video: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error processing video: $e');
    }
  }

  Future<Map<String, dynamic>> processFrame(File frameFile) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/process-frame'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'frame',
          frameFile.path,
        ),
      );

      var response = await request.send();
      var responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        return json.decode(responseData);
      } else {
        throw Exception('Failed to process frame: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error processing frame: $e');
    }
  }
} 