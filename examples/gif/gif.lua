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
