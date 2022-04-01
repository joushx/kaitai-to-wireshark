local gif_proto = Proto("gif", "Gif")

-- field definition
local f_header_magic = ProtoField.bytes("gif.magic", "Magic")
local f_header_version = ProtoField.bytes("gif.version", "Version")
local f_logical_screen_image_width = ProtoField.uint16("gif.image_width", "Image width")
local f_logical_screen_image_height = ProtoField.uint16("gif.image_height", "Image height")
local f_logical_screen_flags = ProtoField.uint8("gif.flags", "Flags")
local f_logical_screen_bg_color_index = ProtoField.uint8("gif.bg_color_index", "Bg color index")
local f_logical_screen_pixel_aspect_ratio = ProtoField.uint8("gif.pixel_aspect_ratio", "Pixel aspect ratio")

-- field registration
gif_proto.fields = {}
table.insert(gif_proto.fields, f_header_magic)
table.insert(gif_proto.fields, f_header_version)
table.insert(gif_proto.fields, f_logical_screen_image_width)
table.insert(gif_proto.fields, f_logical_screen_image_height)
table.insert(gif_proto.fields, f_logical_screen_flags)
table.insert(gif_proto.fields, f_logical_screen_bg_color_index)
table.insert(gif_proto.fields, f_logical_screen_pixel_aspect_ratio)

-- main function
function gif_proto.dissector(tvb, pinfo, root)
  pinfo.cols.protocol = "Gif"
  local tree = root:add(gif_proto, "Gif")
  local offset = 0

  local header = tree:add("header", tvb(offset, 6))
  dissect_header(tvb, pinfo, header)
  local logical_screen = tree:add("logical_screen", tvb(offset, 7))
  dissect_logical_screen(tvb, pinfo, logical_screen)
end

function dissect_header(tvb, pinfo, tree)
  local offset = 0

  local magic = tree:add("magic", tvb(offset, 3))
  dissect_magic(tvb, pinfo, magic)
  local version = tree:add("version", tvb(offset, 3))
  dissect_version(tvb, pinfo, version)
end

function dissect_logical_screen(tvb, pinfo, tree)
  local offset = 0

  tree:add(f_image_width, tvb(offset, 2))
  offset = offset + 1
  tree:add(f_image_height, tvb(offset, 2))
  offset = offset + 1
  tree:add(f_flags, tvb(offset, 1))
  offset = offset + 1
  tree:add(f_bg_color_index, tvb(offset, 1))
  offset = offset + 1
  tree:add(f_pixel_aspect_ratio, tvb(offset, 1))
  offset = offset + 1
end