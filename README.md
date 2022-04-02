# kaitai-to-wireshark
Converts a [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) binary file description to a Wireshark LUA dissector.

## Usage

``./convert.py description.ksy > plugin.lua``

## Supported data types

| Type | Status | Comment |
|------|--------|---------|
| u1   | ✓      |         |
| u2   | ✓      |         |
| u2be | ✓      |         |
| u2le | ✓      |         |
| u4   | ✓      |         |
| u4be | ✓      |         |
| u4le | ✓      |         |
| u8   | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| u8be | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| u8le | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| s1   | ✓      |         |
| s2   | ✓      |         |
| s2be | ✓      |         |
| s2le | ✓      |         |
| s4   | ✓      |         |
| s4be | ✓      |         |
| s4le | ✓      |         |
| s8   | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| s8be | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| s8le | ✓      | Cannot be decoded in Wireshark (Lua uses 32 bit) |
| fxxx | ✗      |         |
| bx   | ✗      |         |
| str  | ✓      |         |
| strz | ✗      |         |

## Supported features

| Feature | Status | Comment |
|---------|--------|---------|
| size    | ✓      | Only static values (no references) |
| types   | ✓      |         |
| contents | ✓     | No check if equal |
| instances | ✓    |         |
| value   | ✗      |         | 
| doc     | ✗      |         |
| Defaul endianess | ✓ |     |
| repeat |  ✗      |         |
| encoding | ✗     |         |
| size-eos | ✗     |         |
| terminator | ✗   |         |
| enums    | ✗     |         |
| if       | ✗     |         |
| switch   | ✗     |         |