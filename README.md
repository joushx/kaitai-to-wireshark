# kaitai-to-wireshark
Converts a [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) binary file description to a Wireshark LUA dissector.

## Usage

``./convert.py description.ksy > plugin.lua``

## Supported data types

| Type | Status | Comment |
|------|--------|---------|
| u1   | ✓      |         |
| u2   | ✓      |         |
| u2be | ✗      |         |
| u2le | ✗      |         |
| u4   | ✓      |         |
| u4be | ✗      |         |
| u4le | ✗      |         |
| u8   | ✓      |         |
| u8be | ✗      |         |
| u8le | ✗      |         |
| s1   | ✓      |         |
| s2   | ✓      |         |
| s2be | ✗      |         |
| s2le | ✗      |         |
| s4   | ✓      |         |
| s4be | ✗      |         |
| s4le | ✗      |         |
| s8   | ✓      |         |
| s8be | ✗      |         |
| s8le | ✗      |         |
| str  | ✓      |         |

## Supported features

| Feature | Status | Comment |
|---------|--------|---------|
| size    | ✓      |         |
| types   | ✓      |         |
| contents | ✓     |         |
| instances | ✗    |         |
| doc     | ✗      |         |