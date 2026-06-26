import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiStreamService {
  static const baseUrl = "http://127.0.0.1:5000";

  static Future<Stream<String>> streamMessage(String message) async {
    final request = http.Request(
      "POST",
      Uri.parse("$baseUrl/chat"),
    );

    request.headers["Content-Type"] = "application/json";

    request.body = jsonEncode({
      "message": message,
    });

    final response = await request.send();

    return response.stream
        .transform(utf8.decoder)
        .transform(const LineSplitter());
  }
}