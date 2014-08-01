function fizzbuzz_for(l, m) {
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

function fizzbuzz_while(l, m){
    n = l;
    while (n <= m){
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
    n = n + 1;
    }
}

function main() {
    var l = 90;
	print "test";
	fizzbuzz_for(10, 100);
	print "did I run fizzbuzz()?";
    print "**************";
    fizzbuzz_while(10, 100);
}