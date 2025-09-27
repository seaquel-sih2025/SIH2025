import 'package:flutter/material.dart';

class RoleSelector extends StatelessWidget {
  final String selectedRole;
  final Function(String) onRoleChanged;

  const RoleSelector({
    super.key,
    required this.selectedRole,
    required this.onRoleChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _RoleCard(
            title: 'Citizen',
            icon: Icons.person,
            color: const Color(0xFF3B82F6),
            gradientColors: const [Color(0xFF60A5FA), Color(0xFF2563EB)],
            isSelected: selectedRole == 'Citizen',
            onTap: () => onRoleChanged('Citizen'),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _RoleCard(
            title: 'Official',
            icon: Icons.security,
            color: const Color(0xFFEF4444),
            gradientColors: const [Color(0xFFF87171), Color(0xFFDC2626)],
            isSelected: selectedRole == 'Official',
            onTap: () => onRoleChanged('Official'),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _RoleCard(
            title: 'Analyst',
            icon: Icons.analytics,
            color: const Color(0xFF8B5CF6),
            gradientColors: const [Color(0xFFA78BFA), Color(0xFF7C3AED)],
            isSelected: selectedRole == 'Analyst',
            onTap: () => onRoleChanged('Analyst'),
          ),
        ),
      ],
    );
  }
}

class _RoleCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final Color color;
  final bool isSelected;
  final VoidCallback onTap;
  final List<Color> gradientColors;

  const _RoleCard({
    required this.title,
    required this.icon,
    required this.color,
    required this.isSelected,
    required this.onTap,
    required this.gradientColors,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
        decoration: BoxDecoration(
          color: isSelected ? color.withValues(alpha: 0.1) : const Color(0xFFF9FAFB),
          border: Border.all(
            color: isSelected ? color : const Color(0xFFE5E7EB),
            width: isSelected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: isSelected
                      ? gradientColors
                      : gradientColors
                          .map((c) => c.withValues(alpha: 0.6))
                          .toList(),
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(
                icon,
                color: Colors.white,
                size: 20,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              title,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w500,
                color: isSelected ? color : const Color(0xFF6B7280),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
