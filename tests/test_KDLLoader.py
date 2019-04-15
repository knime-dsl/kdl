import kdlc
import pytest


def test_exitNode_settings(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.getText.return_value = "42"

    token_l_paren = mocker.MagicMock()
    token_l_paren.getText.return_value = "{"
    token_r_paren = mocker.MagicMock()
    token_r_paren.getText.return_value = "}"
    token_d_quote = mocker.MagicMock()
    token_d_quote.getText.return_value = '"'
    token_n = mocker.MagicMock()
    token_n.getText.return_value = "n"
    token_a = mocker.MagicMock()
    token_a.getText.return_value = "a"
    token_m = mocker.MagicMock()
    token_m.getText.return_value = "m"
    token_e = mocker.MagicMock()
    token_e.getText.return_value = "e"
    token_colon = mocker.MagicMock()
    token_colon.getText.return_value = ":"
    token_b = mocker.MagicMock()
    token_b.getText.return_value = "b"
    token_comma = mocker.MagicMock()
    token_comma.getText.return_value = ","

    token_f = mocker.MagicMock()
    token_f.getText.return_value = "f"
    token_c = mocker.MagicMock()
    token_c.getText.return_value = "c"
    token_t = mocker.MagicMock()
    token_t.getText.return_value = "t"
    token_o = mocker.MagicMock()
    token_o.getText.return_value = "o"
    token_r = mocker.MagicMock()
    token_r.getText.return_value = "r"
    token_y = mocker.MagicMock()
    token_y.getText.return_value = "y"

    token_u = mocker.MagicMock()
    token_u.getText.return_value = "u"
    token_d = mocker.MagicMock()
    token_d.getText.return_value = "d"
    token_l = mocker.MagicMock()
    token_l.getText.return_value = "l"
    token_us = mocker.MagicMock()
    token_us.getText.return_value = "_"

    token_s = mocker.MagicMock()
    token_s.getText.return_value = "s"
    token_i = mocker.MagicMock()
    token_i.getText.return_value = "i"

    token_v = mocker.MagicMock()
    token_v.getText.return_value = "v"

    token_p = mocker.MagicMock()
    token_p.getText.return_value = "p"
    token_one = mocker.MagicMock()
    token_one.getText.return_value = "1"

    token_l_bracket = mocker.MagicMock()
    token_l_bracket.getText.return_value = "["
    token_r_bracket = mocker.MagicMock()
    token_r_bracket.getText.return_value = "]"

    children = [
        token_l_paren,
        token_d_quote,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_f,
        token_a,
        token_c,
        token_t,
        token_o,
        token_r,
        token_y,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_b,
        token_u,
        token_n,
        token_d,
        token_l,
        token_e,
        token_us,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_b,
        token_u,
        token_n,
        token_d,
        token_l,
        token_e,
        token_us,
        token_s,
        token_y,
        token_m,
        token_b,
        token_o,
        token_l,
        token_i,
        token_c,
        token_us,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_b,
        token_u,
        token_n,
        token_d,
        token_l,
        token_e,
        token_us,
        token_v,
        token_e,
        token_r,
        token_s,
        token_i,
        token_o,
        token_n,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_f,
        token_e,
        token_a,
        token_t,
        token_u,
        token_r,
        token_e,
        token_us,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_f,
        token_e,
        token_a,
        token_t,
        token_u,
        token_r,
        token_e,
        token_us,
        token_s,
        token_y,
        token_m,
        token_b,
        token_o,
        token_l,
        token_i,
        token_c,
        token_us,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_f,
        token_e,
        token_a,
        token_t,
        token_u,
        token_r,
        token_e,
        token_us,
        token_v,
        token_e,
        token_r,
        token_s,
        token_i,
        token_o,
        token_n,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_comma,
        token_d_quote,
        token_p,
        token_o,
        token_r,
        token_t,
        token_us,
        token_c,
        token_o,
        token_u,
        token_n,
        token_t,
        token_d_quote,
        token_colon,
        token_one,
        token_comma,
        token_d_quote,
        token_m,
        token_o,
        token_d,
        token_e,
        token_l,
        token_d_quote,
        token_colon,
        token_l_bracket,
        token_r_bracket,
        token_r_paren,
    ]
    ctx.json.return_value.children = children

    listener = kdlc.commands.KDLLoader()

    listener.exitNode_settings(ctx)

    expected_node = kdlc.Node(
        node_id="42",
        name="b",
        factory="b",
        bundle_name="b",
        bundle_symbolic_name="b",
        bundle_version="b",
        feature_name="b",
        feature_symbolic_name="b",
        feature_version="b",
    )
    expected_node.port_count = 1
    expected_node.model = list()

    assert len(listener.nodes) == 1
    assert listener.nodes[0] == expected_node


def test_exitConnection(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    # source_node_port
    source_port_id = mocker.MagicMock()
    source_node.port.return_value.port_id = source_port_id
    source_port_id.return_value.NUMBER.return_value.getText.return_value = "2"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # destination_node_port
    destination_port_id = mocker.MagicMock()
    destination_node.port.return_value.port_id = destination_port_id
    destination_port_id.return_value.NUMBER.return_value.getText.return_value = "4"

    # connection arrow
    ctx.ARROW.return_value = "-->"
    ctx.VARIABLE_ARROW.return_value = None

    listener = kdlc.commands.KDLLoader()

    listener.exitConnection(ctx)

    expected_connection = kdlc.Connection(
        connection_id=0, source_id="1", dest_id="3", source_port="2", dest_port="4"
    )

    assert len(listener.connections) == 1
    assert listener.connections[0] == expected_connection


def test_exitConnection_var(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # connection arrow
    ctx.ARROW.return_value = None
    ctx.VARIABLE_ARROW.return_value = "~~>"

    listener = kdlc.commands.KDLLoader()

    listener.exitConnection(ctx)

    expected_connection = kdlc.Connection(
        connection_id=0, source_id="1", dest_id="3", source_port="0", dest_port="0"
    )

    assert len(listener.connections) == 1
    assert listener.connections[0] == expected_connection


def test_exitConnection_fail(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # connection arrow
    ctx.ARROW.return_value = None
    ctx.VARIABLE_ARROW.return_value = None

    listener = kdlc.commands.KDLLoader()

    with pytest.raises(Exception):
        listener.exitConnection(ctx)


def test_exitGlobal_variables(mocker):
    ctx = mocker.MagicMock()

    token_l_paren = mocker.MagicMock()
    token_l_paren.getText.return_value = "{"
    token_r_paren = mocker.MagicMock()
    token_r_paren.getText.return_value = "}"
    token_d_quote = mocker.MagicMock()
    token_d_quote.getText.return_value = '"'
    token_l_bracket = mocker.MagicMock()
    token_l_bracket.getText.return_value = "["
    token_r_bracket = mocker.MagicMock()
    token_r_bracket.getText.return_value = "]"
    token_colon = mocker.MagicMock()
    token_colon.getText.return_value = ":"
    token_comma = mocker.MagicMock()
    token_comma.getText.return_value = ","

    token_t = mocker.MagicMock()
    token_t.getText.return_value = "t"
    token_one = mocker.MagicMock()
    token_one.getText.return_value = "1"
    token_dot = mocker.MagicMock()
    token_dot.getText.return_value = "."

    children = [
        token_l_bracket,
        token_l_paren,
        token_d_quote,
        token_t,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_t,
        token_d_quote,
        token_r_paren,
        token_comma,
        token_l_paren,
        token_d_quote,
        token_t,
        token_d_quote,
        token_colon,
        token_one,
        token_r_paren,
        token_comma,
        token_l_paren,
        token_d_quote,
        token_t,
        token_d_quote,
        token_colon,
        token_one,
        token_dot,
        token_one,
        token_r_paren,
        token_r_bracket,
    ]

    ctx.json.return_value.children = children
    listener = kdlc.commands.KDLLoader()

    listener.exitGlobal_variables(ctx)

    expected_variables = [{"t": "t"}, {"t": 1}, {"t": 1.1}]

    assert listener.global_variables == expected_variables


def test_exitMeta_settings_connection(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.getText.return_value = "42"
    ctx.STRING.return_value = "test"

    connection = mocker.MagicMock()
    ctx.connection.return_value = [connection]

    source_node = mocker.MagicMock()
    source_node.node_id.return_value.getText.return_value = "1"

    dest_node = mocker.MagicMock()
    dest_node.node_id.return_value.getText.return_value = "2"

    # connection arrow
    connection.ARROW.return_value = "-->"
    connection.VARIABLE_ARROW.return_value = None
    connection.source_node.return_value.node.return_value = source_node
    connection.des_node.return_value.node.return_value = dest_node

    listener = kdlc.commands.KDLLoader()
    listener.exitMeta_settings(ctx)

    assert len(listener.nodes) == 1
    assert len(listener.nodes[0].connections)


def test_exitMeta_settings_var_connection(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.getText.return_value = "42"
    ctx.STRING.return_value = "test"

    connection = mocker.MagicMock()
    ctx.connection.return_value = [connection]

    source_node = mocker.MagicMock()
    source_node.node_id.return_value.getText.return_value = "1"

    dest_node = mocker.MagicMock()
    dest_node.node_id.return_value.getText.return_value = "2"

    # connection arrow
    connection.ARROW.return_value = None
    connection.VARIABLE_ARROW.return_value = "~~>"
    connection.source_node.return_value.node.return_value = source_node
    connection.des_node.return_value.node.return_value = dest_node

    listener = kdlc.commands.KDLLoader()
    listener.exitMeta_settings(ctx)

    assert len(listener.nodes) == 1
    assert len(listener.nodes[0].connections)


def test_exitMeta_settings_metaconnection_in(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.getText.return_value = "42"
    ctx.STRING.return_value = "test"

    connection = mocker.MagicMock()

    ctx.meta_connection.return_value = [connection]

    meta_in_node = mocker.MagicMock()
    NUMBER = mocker.MagicMock()
    NUMBER.return_value.getText.return_value = "1"
    meta_in_node.port.return_value.port_id.return_value = NUMBER

    dest_node = mocker.MagicMock()
    NUMBER = mocker.MagicMock()
    NUMBER.return_value.getText.return_value = "2"
    dest_node.node_id.return_value.getText.return_value = "2"
    dest_node.port.return_value.port_id.return_value = NUMBER

    # connection arrow
    connection.meta_in_node = meta_in_node

    listener = kdlc.commands.KDLLoader()
    listener.exitMeta_settings(ctx)

    assert len(listener.nodes) == 1
    assert len(listener.nodes[0].connections)


def test_exitMeta_settings_metaconnection_out(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.getText.return_value = "42"
    ctx.STRING.return_value = "test"

    connection = mocker.MagicMock()

    ctx.meta_connection.return_value = [connection]

    meta_out_node = mocker.MagicMock()
    NUMBER = mocker.MagicMock()
    NUMBER.return_value.getText.return_value = "1"
    meta_out_node.port.return_value.port_id.return_value = NUMBER

    source_node = mocker.MagicMock()
    source_node.node_id.return_value.getText.return_value = "2"
    NUMBER = mocker.MagicMock()
    NUMBER.return_value.getText.return_value = "2"
    source_node.port.return_value.port_id.return_value = NUMBER

    # connection arrow
    connection.meta_out_node = meta_out_node

    listener = kdlc.commands.KDLLoader()
    listener.exitMeta_settings(ctx)

    assert len(listener.nodes) == 1
    assert len(listener.nodes[0].connections)
