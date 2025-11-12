#!/bin/bash
################################################################################
# GV Application Deployment Script (Using Pre-compiled Classes)
################################################################################

set -e  # Exit on error

echo "=========================================="
echo "GV Application - Pre-compiled Deployment"
echo "=========================================="
echo ""
echo "NOTE: Due to decompilation artifacts in some service files,"
echo "this script uses the original pre-compiled .class files"
echo "which are known to work correctly."
echo ""

# Configuration
APP_NAME="GV"
DIST_DIR="dist"
WEBAPP_DIR="webapp"
LIB_DIR="lib"
ORIGINAL_CLASSES="../webapps/GV/WEB-INF/classes"

# Clean previous build
echo "[1/4] Cleaning previous build..."
rm -rf $DIST_DIR
mkdir -p $DIST_DIR/$APP_NAME/WEB-INF/classes
mkdir -p $DIST_DIR/$APP_NAME/WEB-INF/lib

# Create WAR structure using pre-compiled classes
echo ""
echo "[2/4] Creating WAR structure..."

# Copy pre-compiled classes from original deployment
echo "   Copying pre-compiled classes..."
cp -r $ORIGINAL_CLASSES/* $DIST_DIR/$APP_NAME/WEB-INF/classes/

# Copy configuration files
echo "   Copying configuration files..."
cp $WEBAPP_DIR/WEB-INF/web.xml $DIST_DIR/$APP_NAME/WEB-INF/

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

echo "   ✓ WAR structure created"

# Create WAR file
echo ""
echo "[3/4] Creating WAR file..."
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

# Deploy to Tomcat
echo ""
echo "[4/4] Deploying to Tomcat..."
TOMCAT_HOME="/home/star/work/apache-tomcat-8.5.57"
WEBAPPS_DIR="$TOMCAT_HOME/webapps"

if [ ! -d "$TOMCAT_HOME" ]; then
    echo "   ERROR: Tomcat not found at: $TOMCAT_HOME"
    exit 1
fi

# Backup existing deployment
if [ -d "$WEBAPPS_DIR/$APP_NAME" ] || [ -f "$WEBAPPS_DIR/$APP_NAME.war" ]; then
    BACKUP_DIR="$WEBAPPS_DIR/${APP_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
    echo "   Creating backup at: $BACKUP_DIR"

    mkdir -p "$BACKUP_DIR"
    [ -d "$WEBAPPS_DIR/$APP_NAME" ] && mv "$WEBAPPS_DIR/$APP_NAME" "$BACKUP_DIR/"
    [ -f "$WEBAPPS_DIR/$APP_NAME.war" ] && mv "$WEBAPPS_DIR/$APP_NAME.war" "$BACKUP_DIR/"
fi

# Deploy
cp "$DIST_DIR/$APP_NAME.war" "$WEBAPPS_DIR/"
echo "   ✓ Deployed to: $WEBAPPS_DIR/"

# Summary
echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  http://localhost:8089/GV/input.jsp"
echo ""
echo "Note: Check your Tomcat server.xml for the correct port"
echo "      (default is 8089 for service 'Catalina2')"
echo ""
echo "To start/restart Tomcat:"
echo "  $TOMCAT_HOME/bin/shutdown.sh && $TOMCAT_HOME/bin/startup.sh"
echo ""
echo "To view logs:"
echo "  tail -f $TOMCAT_HOME/logs/catalina.out"
echo ""
