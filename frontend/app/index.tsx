import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { router } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

type ModeButtonProps = {
  icon: keyof typeof MaterialIcons.glyphMap;
  title: string;
  description: string;
  onPress: () => void;
  variant: 'primary' | 'secondary';
  tint: string;
  textColor: string;
  mutedColor: string;
};

function ModeButton({
  icon,
  title,
  description,
  onPress,
  variant,
  tint,
  textColor,
  mutedColor,
}: ModeButtonProps) {
  const isPrimary = variant === 'primary';

  return (
    <Pressable
      style={({ pressed }) => [
        styles.modeButton,
        isPrimary
          ? { backgroundColor: tint }
          : { backgroundColor: 'transparent', borderColor: tint, borderWidth: 2 },
        pressed && styles.modeButtonPressed,
      ]}
      onPress={onPress}>
      <View
        style={[
          styles.iconCircle,
          { backgroundColor: isPrimary ? 'rgba(255,255,255,0.2)' : `${tint}18` },
        ]}>
        <MaterialIcons name={icon} size={28} color={isPrimary ? '#fff' : tint} />
      </View>
      <View style={styles.modeButtonText}>
        <ThemedText
          style={styles.modeButtonTitle}
          lightColor={isPrimary ? '#fff' : textColor}
          darkColor={isPrimary ? '#151718' : textColor}>
          {title}
        </ThemedText>
        <ThemedText
          style={styles.modeButtonDescription}
          lightColor={isPrimary ? 'rgba(255,255,255,0.85)' : mutedColor}
          darkColor={isPrimary ? 'rgba(21,23,24,0.75)' : mutedColor}>
          {description}
        </ThemedText>
      </View>
      <MaterialIcons
        name="chevron-right"
        size={24}
        color={isPrimary ? '#fff' : tint}
      />
    </Pressable>
  );
}

export default function LandingScreen() {
  const colorScheme = useColorScheme() ?? 'light';
  const colors = Colors[colorScheme];

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.hero}>
          <View style={[styles.logoBadge, { backgroundColor: `${colors.tint}18` }]}>
            <MaterialIcons name="visibility" size={36} color={colors.tint} />
          </View>
          <ThemedText type="title" style={styles.title}>
            lastseen
          </ThemedText>
          <ThemedText style={styles.tagline} lightColor={colors.icon} darkColor={colors.icon}>
            Remember where you put things
          </ThemedText>
          <ThemedText style={styles.description} lightColor={colors.icon} darkColor={colors.icon}>
            Turn one phone into a room camera and use another to ask where your stuff is.
          </ThemedText>
        </View>

        <View style={styles.actions}>
          <ModeButton
            icon="photo-camera"
            title="Use this phone as camera"
            description="Scan the room and log where objects are placed"
            variant="primary"
            tint={colors.tint}
            textColor={colors.text}
            mutedColor={colors.icon}
            onPress={() => router.push('/camera')}
          />
          <ModeButton
            icon="search"
            title="Ask where something is"
            description={'Try "Where is my calculator?"'}
            variant="secondary"
            tint={colors.tint}
            textColor={colors.text}
            mutedColor={colors.icon}
            onPress={() => router.push('/ask')}
          />
        </View>

        <ThemedText style={styles.privacyNote} lightColor={colors.icon} darkColor={colors.icon}>
          Only scan spaces you have permission to record. Avoid private areas during testing.
        </ThemedText>
      </SafeAreaView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: 24,
    paddingBottom: 24,
    justifyContent: 'space-between',
  },
  hero: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 12,
    paddingTop: 24,
  },
  logoBadge: {
    width: 72,
    height: 72,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  title: {
    fontSize: 44,
    lineHeight: 52,
    letterSpacing: -1.5,
  },
  tagline: {
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
  },
  description: {
    fontSize: 15,
    lineHeight: 22,
    textAlign: 'center',
    maxWidth: 320,
    marginTop: 4,
  },
  actions: {
    gap: 14,
    width: '100%',
  },
  modeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    padding: 18,
    borderRadius: 16,
  },
  modeButtonPressed: {
    opacity: 0.88,
    transform: [{ scale: 0.985 }],
  },
  iconCircle: {
    width: 48,
    height: 48,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  modeButtonText: {
    flex: 1,
    gap: 4,
  },
  modeButtonTitle: {
    fontSize: 16,
    fontWeight: '700',
    lineHeight: 22,
  },
  modeButtonDescription: {
    fontSize: 13,
    lineHeight: 18,
  },
  privacyNote: {
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
    marginTop: 20,
    paddingHorizontal: 12,
  },
});
