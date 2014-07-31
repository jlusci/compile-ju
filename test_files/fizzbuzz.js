function fizzbuzz(l, m) {
    for(var n = l; n <= m; n = n+1){
        if (n % 15 == 0) {
			print "FizzBuzz";
		}
		else {
            if (n % 3 == 0) {
                print "Fizz";
            }
            else {
                if(n % 5 == 0) {
                    print "Buzz";
                }
                else {
                    print n;
                }
            }
		}
	}
}

function main() {
    var l = 90;
	print "test";
	fizzbuzz(90, 100);
	print "did I run fizzbuzz()?";
}