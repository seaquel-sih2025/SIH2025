class UserModel {
  final String id;
  final String email;
  final String username;
  final String role;
  final String? firstName;
  final String? lastName;
  final String? profileImage;
  final DateTime createdAt;
  final DateTime updatedAt;
  final bool isVerified;

  UserModel({
    required this.id,
    required this.email,
    required this.username,
    required this.role,
    this.firstName,
    this.lastName,
    this.profileImage,
    required this.createdAt,
    required this.updatedAt,
    this.isVerified = false,
  });

  // Create UserModel from JSON
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? json['_id'] ?? '',
      email: json['email'] ?? '',
      username: json['username'] ?? '',
      role: json['role'] ?? 'citizen',
      firstName: json['firstName'] ?? json['first_name'],
      lastName: json['lastName'] ?? json['last_name'],
      profileImage: json['profileImage'] ?? json['profile_image'],
      createdAt: DateTime.tryParse(json['createdAt'] ?? json['created_at'] ?? '') ?? DateTime.now(),
      updatedAt: DateTime.tryParse(json['updatedAt'] ?? json['updated_at'] ?? '') ?? DateTime.now(),
      isVerified: json['isVerified'] ?? json['is_verified'] ?? false,
    );
  }

  // Convert UserModel to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'role': role,
      'firstName': firstName,
      'lastName': lastName,
      'profileImage': profileImage,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
      'isVerified': isVerified,
    };
  }

  // Get full name
  String get fullName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    } else if (firstName != null) {
      return firstName!;
    } else if (lastName != null) {
      return lastName!;
    } else {
      return username;
    }
  }

  // Get display name (prioritizes full name, falls back to username)
  String get displayName {
    final name = fullName;
    return name.isNotEmpty ? name : username;
  }

  // Check if user has specific role
  bool hasRole(String roleToCheck) {
    return role.toLowerCase() == roleToCheck.toLowerCase();
  }

  // Check if user is citizen
  bool get isCitizen => hasRole('citizen');

  // Check if user is official
  bool get isOfficial => hasRole('official');

  // Check if user is analyst
  bool get isAnalyst => hasRole('analyst');

  // Create a copy with updated fields
  UserModel copyWith({
    String? id,
    String? email,
    String? username,
    String? role,
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? createdAt,
    DateTime? updatedAt,
    bool? isVerified,
  }) {
    return UserModel(
      id: id ?? this.id,
      email: email ?? this.email,
      username: username ?? this.username,
      role: role ?? this.role,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      profileImage: profileImage ?? this.profileImage,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      isVerified: isVerified ?? this.isVerified,
    );
  }

  @override
  String toString() {
    return 'UserModel(id: $id, email: $email, username: $username, role: $role, fullName: $fullName, isVerified: $isVerified)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is UserModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
