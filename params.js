function foo(a) {
    print "this is inside foo";
    print a;
    x = a + 5*9+1;
    print x;
}

function main() {
    print "here is where i call foo from main";
    print "begin test";
    foo(5);
    print "end test";
}