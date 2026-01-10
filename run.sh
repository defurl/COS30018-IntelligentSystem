#!/bin/bash

# Configuration
LIB_DIR="./lib"
SRC_DIR="./src"
OUT_DIR="./bin"
JADE_JAR="$LIB_DIR/jade.jar"
COMMONS_CODEC_JAR="$LIB_DIR/commons-codec.jar"
CLASSPATH="$JADE_JAR:$COMMONS_CODEC_JAR:$OUT_DIR"

# Step 1: Create output directory
mkdir -p "$OUT_DIR"

# Step 2: Compile everything recursively in src/
echo "--- Compiling all agents in $SRC_DIR (including subfolders) ---"
find "$SRC_DIR" -name "*.java" > sources.txt
if [ -s sources.txt ]; then
    javac -cp "$CLASSPATH" -d "$OUT_DIR" @sources.txt
    rm sources.txt
else
    echo "No Java files found in $SRC_DIR"
    rm sources.txt
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "Compilation successful."
else
    echo "Compilation failed."
    exit 1
fi

# Step 3: Run JADE
# Usage: ./run.sh [-gui] [agent_name:class_name;agent2:class2]

GUI_FLAG=""
AGENTS_LIST=""

for arg in "$@"; do
    if [ "$arg" == "-gui" ]; then
        GUI_FLAG="-gui"
    else
        AGENTS_LIST="$arg"
    fi
done

# Default agent fallback
if [ -z "$AGENTS_LIST" ] && [ -f "$OUT_DIR/week1/HelloAgent.class" ]; then
    AGENTS_LIST="hello:week1.HelloAgent"
fi

echo "--- Starting JADE Container ---"
if [ -z "$AGENTS_LIST" ]; then
    echo "Running JADE (No agents specified)..."
    java -cp "$CLASSPATH" jade.Boot $GUI_FLAG
else
    echo "Running JADE with agents: $AGENTS_LIST"
    java -cp "$CLASSPATH" jade.Boot $GUI_FLAG -agents "$AGENTS_LIST"
fi
