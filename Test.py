# The spaces in the following expected outputs are just for readability.
# They will be ignored during comparison.

# Test Case 1: Declaration and Assignment
test_input_1 = """
var x : Integer;
var y : Boolean := False;
var variable :Boolean;
Put(variable);
var Booleannn : Boolean := True;
"""
expected_output_1 = """
Block([
Decl(Identifier(x),Type(Integer),None),
Decl(Identifier(y),Type(Boolean),Boolean(False)),
Decl(Identifier(variable),Type(Boolean),None),
Put(Identifier(variable)),
Decl(Identifier(Booleannn),Type(Boolean),Boolean(True))
])
"""

# Test Case 2: Declaration and Assignment
test_input_2 = """
var x : Integer := True;
"""
expected_output_2 = """
Invalid
"""

# Test Case 3: Declaration and Assignment
test_input_3 = """
var x : Integer;
var x : Boolean;
"""
expected_output_3 = """
Invalid
"""

# Test Case 4: scoping
test_input_4 = """
var x : Integer := 10;
while x > 0 loop
    var y : Boolean := True;
    Put(x);
    Put(y);
end loop;
"""
expected_output_4 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(10)),
    WhileLoop(Comparison(Identifier(x),>,Integer(0)),
        Block([
            Decl(Identifier(y),Type(Boolean),Boolean(True)),
            Put(Identifier(x)),
            Put(Identifier(y))
        ])
    )
])
"""

# Test Case 5: scoping
test_input_5 = """
var x : Integer;
if x > 1 then
    Put(x);
else
    x := x - 1;
end if;
"""
expected_output_5 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    If(Comparison(Identifier(x),>,Integer(1)),
        Block([Put(Identifier(x))]),
        Block([
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)]))
        ])
    )
])
"""

# Test Case 6: scoping
test_input_6 = """
var x : Boolean := False;
while x loop
    var x : Integer := 10;
    x := x - 1;
    Put(x);
end loop;
x := True;
"""
expected_output_6 = """
Block([
    Decl(Identifier(x),Type(Boolean),Boolean(False)),
    WhileLoop(Identifier(x),
        Block([
            Decl(Identifier(x),Type(Integer),Integer(10)),
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)])),
            Put(Identifier(x))
        ])
    ),
    Assign(Identifier(x),Boolean(True))
])
"""

# Test Case 7: scoping
test_input_7 = """
while False loop
    var x : Integer;
end loop;
x := 5;
"""
expected_output_7 = """
Invalid
"""

# Test Case 8: scoping
test_input_8 = """
if True then
    var i : Integer;
    i := 1;
else
    var i : Boolean;
    i := True;
end if;
"""
expected_output_8 = """
Block([
    If(Boolean(True),
        Block([
            Decl(Identifier(i),Type(Integer),None),
            Assign(Identifier(i),Integer(1))
        ]),
        Block([
            Decl(Identifier(i),Type(Boolean),None),
            Assign(Identifier(i),Boolean(True))
        ])
    )
])
"""

# Test Case 9: type compatibility
test_input_9 = """
var x : Integer := 1;
var y : Integer := 2;
var z : Integer;
x := y + z;
var a : Boolean := True;
var b : Boolean := False;
Put(a and (b or False));
"""
expected_output_9 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(1)),
    Decl(Identifier(y),Type(Integer),Integer(2)),
    Decl(Identifier(z),Type(Integer),None),
    Assign(Identifier(x),Term([Identifier(y),+,Identifier(z)])),
    Decl(Identifier(a),Type(Boolean),Boolean(True)),
    Decl(Identifier(b),Type(Boolean),Boolean(False)),
    Put(And([Identifier(a),Or([Identifier(b),Boolean(False)])]))
])
"""

# Test Case 10: type compatibility
test_input_10 = """
var b1 : Boolean;
var b2 : Boolean;
var b3 : Boolean;
var i1 : Integer;
var i2 : Integer;
var i3 : Integer;
b1 := (b2 or b3) and i1 /= i2 or i2 mod i3 = 0;
"""
expected_output_10 = """
Block([
    Decl(Identifier(b1),Type(Boolean),None),
    Decl(Identifier(b2),Type(Boolean),None),
    Decl(Identifier(b3),Type(Boolean),None),
    Decl(Identifier(i1),Type(Integer),None),
    Decl(Identifier(i2),Type(Integer),None),
    Decl(Identifier(i3),Type(Integer),None),
    Assign(Identifier(b1),
        Or([
            And([
                Or([Identifier(b2),Identifier(b3)]),
                Comparison(Identifier(i1),/=,Identifier(i2))
            ]),
            Comparison(
                Factor([Identifier(i2),mod,Identifier(i3)]),
                =,
                Integer(0)
            )
        ])
    )
])
"""

# Test Case 11: type compatibility
test_input_11 = """
var x : Integer;
var y : Boolean;
x := 1 + y;
"""
expected_output_11 = """
Invalid
"""

# Test Case 12: type compatibility
test_input_12 = """
var x : Integer;
var y : Boolean;
y := x /= 0;
"""
expected_output_12 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    Decl(Identifier(y),Type(Boolean),None),
    Assign(Identifier(y),Comparison(Identifier(x),/=,Integer(0)))
])
"""

# Test Case 13: combined
test_input_13 = """
var x : Integer;
if x mod 2 = 0 then
    Put(1 + x);
else
    var x : Boolean := True;
    Put(x or False);
end if;
"""
expected_output_13 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    If(Comparison(Factor([Identifier(x),mod,Integer(2)]),=,Integer(0)),
        Block([
            Put(Term([Integer(1),+,Identifier(x)]))
        ]),
        Block([
            Decl(Identifier(x),Type(Boolean),Boolean(True)),
            Put(Or([Identifier(x),Boolean(False)]))
        ])
    )
])
"""

# Test Case 14: combined
test_input_14 = """
var x : Boolean;
while x loop
    if x then
        x := False;
    else
        var x : Integer;
        x := True;
    end if;
end loop;
"""
expected_output_14 = """
Invalid
"""

# Test Case 15: combined
test_input_15 = """
var x : Integer;
var y : Boolean;
var z : Boolean;
if (x + 1) > 0 and (y or z) then
    x := x - 1;
    if z then
        var y : Integer;
    end if;
    y := False;
end if;
"""
expected_output_15 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    Decl(Identifier(y),Type(Boolean),None),
    Decl(Identifier(z),Type(Boolean),None),
    If(And([
            Comparison(Term([Identifier(x),+,Integer(1)]),>,Integer(0)),
            Or([Identifier(y),Identifier(z)])
            ]),
        Block([
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)])),
            If(Identifier(z),
                Block([Decl(Identifier(y),Type(Integer),None)]),
                None),
            Assign(Identifier(y),Boolean(False))
        ]),
        None
    )
])
"""
