# kaitai-to-wireshark
Converts a [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) binary file description to a Wireshark LUA dissector.

##Usage##

``./convert.py description.ksy > plugin.lua``

Please note that the result is not a finished wireshark plugin but rather a prototype for further customization. For instance it always uses the `bytes` type for fields.

Please replace `<port>` with the port to register the dissector for.

##Example##

A Kaitai Struct file:

```yaml
meta:
  id: gif
  file-extension: gif
  endian: le
seq:
  - id: header
    type: header
  - id: logical_screen
    type: logical_screen
types:
  header:
    seq:
      - id: magic
        contents: 'GIF'
      - id: version
        size: 3
  logical_screen:
    seq:
      - id: image_width
        type: u2
      - id: image_height
        type: u2
      - id: flags
        type: u1
      - id: bg_color_index
        type: u1
      - id: pixel_aspect_ratio
        type: u1
```

The resulting lua file to be used with Wireshark:

```lua
gif_proto = Proto("gif","gif file")

local f = gif_proto.fields

-- field declaration
f.header = ProtoField.bytes("gif.header", "header")
f.logical_screen = ProtoField.bytes("gif.logical_screen", "logical_screen")
f.magic = ProtoField.bytes("gif.header.magic", "magic")
f.version = ProtoField.bytes("gif.header.version", "version")
f.image_width = ProtoField.bytes("gif.logical_screen.image_width", "image_width")
f.image_height = ProtoField.bytes("gif.logical_screen.image_height", "image_height")
f.flags = ProtoField.bytes("gif.logical_screen.flags", "flags")
f.bg_color_index = ProtoField.bytes("gif.logical_screen.bg_color_index", "bg_color_index")
f.pixel_aspect_ratio = ProtoField.bytes("gif.logical_screen.pixel_aspect_ratio", "pixel_aspect_ratio")

-- main function
function modes_proto.dissector(buffer,pinfo,tree)
  pinfo.cols.protocol = "gif"

  main = tree:add(gif_proto, "gif file")

  local header = main:add(f.header,"header")
  header:add(buffer(0,3), f.magic)
  header:add(buffer(3,3), f.version)
  local logical_screen = main:add(f.logical_screen,"logical_screen")
  logical_screen:add(buffer(0,2), f.image_width)
  logical_screen:add(buffer(2,2), f.image_height)
  logical_screen:add(buffer(4,1), f.flags)
  logical_screen:add(buffer(5,1), f.bg_color_index)
  logical_screen:add(buffer(6,1), f.pixel_aspect_ratio)
end

tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(<port>, gif_proto)
```

##Limitations##

Currently the script is just a proof-of-concept, very hacky and only converts a few basic data types: `u1`, `u2`, `u3`, fields with `contents` and fields with `size`. It is basically a template that gets filled with data.
