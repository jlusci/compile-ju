function foo(a) {
    print "this is inside foo";
    print "aww yeah. ¢ra§y ©hàræçtër$? ñø ¶rõßlem$!";
    print a;
    x = a + 5*9+1;
    print x;
}

function main() {
    print "here is where i call foo from main";
    print "begin test";
    var y = foo(5);
    print y;
    print "end test";
}
