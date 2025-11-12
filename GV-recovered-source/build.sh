#!/bin/bash
################################################################################
# GV Application Build Script
################################################################################

set -e  # Exit on error

echo "=========================================="
echo "GV Application Build Script"
echo "=========================================="

# Configuration
APP_NAME="GV"
BUILD_DIR="build"
DIST_DIR="dist"
SRC_DIR="src"
LIB_DIR="lib"
WEBAPP_DIR="webapp"

# Clean previous build
echo ""
echo "[1/5] Cleaning previous build..."
rm -rf $BUILD_DIR $DIST_DIR
mkdir -p $BUILD_DIR
mkdir -p $DIST_DIR

# Compile Java sources
echo ""
echo "[2/5] Compiling Java sources..."
CLASSPATH=""
for jar in $LIB_DIR/*.jar; do
    CLASSPATH="$CLASSPATH:$jar"
done

# Add Tomcat servlet-api
TOMCAT_LIB="/home/star/work/apache-tomcat-8.5.57/lib"
if [ -f "$TOMCAT_LIB/servlet-api.jar" ]; then
    CLASSPATH="$CLASSPATH:$TOMCAT_LIB/servlet-api.jar"
fi

echo "   Compiling with classpath: $CLASSPATH"

# Compile only essential files (exclude broken decompiled copies)
# Only ViewServiceR2 is actually used by the application
JAVA_FILES="
    $SRC_DIR/com/gv/model/Product.java
    $SRC_DIR/com/gv/model/Material.java
    $SRC_DIR/com/gv/model/Scheme.java
    $SRC_DIR/com/gv/constant/Constant.java
    $SRC_DIR/com/gv/tool/CommonTools.java
    $SRC_DIR/com/gv/tool/DecimalMath.java
    $SRC_DIR/com/gv/service/ViewServiceR2.java
    $SRC_DIR/com/gv/action/ViewAction.java
"

javac -encoding UTF-8 \
      -source 1.7 -target 1.7 \
      -cp "$CLASSPATH" \
      -d $BUILD_DIR \
      $JAVA_FILES

if [ $? -eq 0 ]; then
    echo "   ✓ Compilation successful"
else
    echo "   ✗ Compilation failed"
    exit 1
fi

# Create WAR structure
echo ""
echo "[3/5] Creating WAR structure..."
mkdir -p $DIST_DIR/$APP_NAME/WEB-INF/classes
mkdir -p $DIST_DIR/$APP_NAME/WEB-INF/lib

# Copy compiled classes
echo "   Copying compiled classes..."
cp -r $BUILD_DIR/* $DIST_DIR/$APP_NAME/WEB-INF/classes/

# Copy configuration files
echo "   Copying configuration files..."
cp $WEBAPP_DIR/WEB-INF/web.xml $DIST_DIR/$APP_NAME/WEB-INF/
cp $WEBAPP_DIR/WEB-INF/classes/*.xml $DIST_DIR/$APP_NAME/WEB-INF/classes/ 2>/dev/null || true

# Copy libraries
echo "   Copying libraries..."
cp $LIB_DIR/*.jar $DIST_DIR/$APP_NAME/WEB-INF/lib/

# Copy web resources
echo "   Copying web resources..."
cp $WEBAPP_DIR/*.jsp $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp $WEBAPP_DIR/*.html $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp $WEBAPP_DIR/*.jpg $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp $WEBAPP_DIR/*.png $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp $WEBAPP_DIR/*.gif $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp -r $WEBAPP_DIR/css $DIST_DIR/$APP_NAME/ 2>/dev/null || true
cp -r $WEBAPP_DIR/js $DIST_DIR/$APP_NAME/ 2>/dev/null || true

# Create WAR file
echo ""
echo "[4/5] Creating WAR file..."
cd $DIST_DIR/$APP_NAME
jar -cvf ../$APP_NAME.war * > /dev/null 2>&1
cd ../..

if [ -f "$DIST_DIR/$APP_NAME.war" ]; then
    WAR_SIZE=$(du -h $DIST_DIR/$APP_NAME.war | cut -f1)
    echo "   ✓ WAR file created: $APP_NAME.war ($WAR_SIZE)"
else
    echo "   ✗ WAR creation failed"
    exit 1
fi

# Summary
echo ""
echo "[5/5] Build Summary"
echo "=========================================="
echo "Build directory:  $BUILD_DIR/"
echo "WAR file:         $DIST_DIR/$APP_NAME.war"
echo "Exploded WAR:     $DIST_DIR/$APP_NAME/"
echo ""
echo "✓ Build completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Deploy: ./deploy.sh"
echo "  2. Or manually copy: cp dist/GV.war /path/to/tomcat/webapps/"
echo ""
