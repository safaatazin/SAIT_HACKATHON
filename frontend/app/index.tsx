import { router } from 'expo-router';
import { Pressable, StyleSheet } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

export default function LandingScreen() {
  const colorScheme = useColorScheme() ?? 'light';
  const tint = Colors[colorScheme].tint;

  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title" style={styles.title}>
        lastseen
      </ThemedText>
      <Pressable
        style={({ pressed }) => [
          styles.button,
          { backgroundColor: tint, opacity: pressed ? 0.85 : 1 },
        ]}
        onPress={() => router.replace('/(tabs)')}>
        <ThemedText lightColor="#fff" darkColor="#151718" style={styles.buttonText}>
          Start
        </ThemedText>
      </Pressable>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    gap: 48,
  },
  title: {
    fontSize: 48,
    lineHeight: 56,
    letterSpacing: -1,
  },
  button: {
    paddingHorizontal: 48,
    paddingVertical: 16,
    borderRadius: 12,
    minWidth: 160,
    alignItems: 'center',
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '600',
  },
});
