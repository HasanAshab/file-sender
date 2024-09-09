@echo off
setlocal
set APP_HOME=%~dp0
set EXE=java
set EXTRA_ARGS=
if not "%JAVA_OPTS%"=="" set EXTRA_ARGS=%JAVA_OPTS%
"%EXE%" %EXTRA_ARGS% -cp "%APP_HOME%gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*
endlocal
