#!/usr/bin/env sh
# Gradle Wrapper Script
APP_HOME=$(dirname "$0")
EXE="java"
EXTRA_ARGS=""
if [ -n "$JAVA_OPTS" ]; then
  EXTRA_ARGS="$JAVA_OPTS"
fi
exec "$EXE" $EXTRA_ARGS -cp "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"
