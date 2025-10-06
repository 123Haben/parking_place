# Command Processing System

## Overview

This module implements a JSON-based command system to control devices such as GATE, LED, MOTION, and DISTANCE sensors. Commands are sent and received in JSON format.

## JSON Command Format

### Input (Request)

```json
{
  "deviceName": "DEVICE_TYPE",
  "deviceId": "ID",
  "actionName": "ACTION",
  "argument": "OPTIONAL_ARGUMENT"
}
```

### Output (Response)

```json
{
  "deviceName": "DEVICE_TYPE",
  "deviceId": "ID",
  "deviceResponse": "RESULT"
}
```

## Supported Devices

### GATE

| Action     | Argument | Response        |
| ---------- | -------- | --------------- |
| OPEN       | -        | OPENED          |
| CLOSE      | -        | CLOSED          |
| GET_STATUS | -        | OPENED / CLOSED |

### MOTION

| Action     | Argument | Response           |
| ---------- | -------- | ------------------ |
| GET_STATUS | -        | MOTION / NO MOTION |

### LED

| Action     | Argument                   | Response                   |
| ---------- | -------------------------- | -------------------------- |
| GET_STATUS | -                          | FREE / OCCUPIED / RESERVED |
| SET_STATUS | FREE / OCCUPIED / RESERVED | FREE / OCCUPIED / RESERVED |

### DISTANCE

| Action    | Argument | Response        |
| --------- | -------- | --------------- |
| GET_VALUE | -        | Float as string |

## Examples

**Open GATE**

```json
{"deviceName":"GATE","deviceId":"1","actionName":"OPEN"}
```

**Response**

```json
{"deviceName":"GATE","deviceId":"1","deviceResponse":"OPENED"}
```

**Set LED Status**

```json
{"deviceName":"LED","deviceId":"2","actionName":"SET_STATUS","argument":"OCCUPIED"}
```

**Response**

```json
{"deviceName":"LED","deviceId":"2","deviceResponse":"OCCUPIED"}
```

**Get DISTANCE Value**

```json
{"deviceName":"DISTANCE","deviceId":"1","actionName":"GET_VALUE"}
```

**Response**

```json
{"deviceName":"DISTANCE","deviceId":"1","deviceResponse":"34.57"}
```

## C++ Structures

```cpp
struct CommandModel {
    String deviceName;
    String deviceId;
    String actionName;
    String argument; // optional
};

struct CommandResponse {
    String deviceName;
    String deviceId;
    String deviceResponse;
};
```

## Methods

* `CommandModel Command::fromJson(const String &jsonString)` - parses JSON into CommandModel
* `JsonDocument Command::toJson(const CommandResponse &commandResponse)` - converts response to JSON
* `JsonDocument Command::sendAndResponse(const CommandModel &commandModel)` - executes command and returns response
