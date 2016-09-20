{{data.meta.id}}_proto = Proto("{{data.meta.id}}","{{data.meta.id}} file")

local f = {{data.meta.id}}_proto.fields

-- field declaration
{% for item in data.seq %}
f.{{item.id}} = ProtoField.bytes("{{data.meta.id}}.{{item.id}}", "{{item.id}}")
{% endfor %}
{% for item in data["types"].items() %}
{% for seqitem in item.1.seq %}
f.{{seqitem.id}} = ProtoField.bytes("{{data.meta.id}}.{{item.0}}.{{seqitem.id}}", "{{seqitem.id}}")
{% endfor %}
{% endfor %}

-- main function
function modes_proto.dissector(buffer,pinfo,tree)
  pinfo.cols.protocol = "{{data.meta.id}}"

  main = tree:add({{data.meta.id}}_proto, "{{data.meta.id}} file")

  {% set offset = 0 %}
  {% for item in data["types"].items() %}
  local {{item.0}} = main:add(f.{{item.0}},"{{item.0}}")
  {% for seqitem in item.1.seq %}
  {% if seqitem.type == "u1" %}
  {{item.0}}:add(buffer({{offset}},1), f.{{seqitem.id}})
  {% set offset = offset+1 %}
  {% elif seqitem.type == "u2" %}
  {{item.0}}:add(buffer({{offset}},2), f.{{seqitem.id}})
  {% set offset = offset+2 %}
  {% elif seqitem.type == "u3" %}
  {{item.0}}:add(buffer({{offset}},3), f.{{seqitem.id}})
  {% set offset = offset+3 %}
  {% elif seqitem.contents %}
  {{item.0}}:add(buffer({{offset}},{{seqitem.contents|length}}), f.{{seqitem.id}})
  {% set offset = offset + seqitem.contents|length %}
  {% elif seqitem.size %}
  {{item.0}}:add(buffer({{offset}},{{seqitem.size}}), f.{{seqitem.id}})
  {% set offset = offset + seqitem.size %}
  {% endif %}
  {% endfor %}
  {% endfor %}
end

tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(<port>, {{data.meta.id}}_proto)
