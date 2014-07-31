function main() {
	print "Hello world";
	print 3+-3;
	var x = 2;
	print x;
	print x+5*9;
	var x = x+3;
	print x;
	var y = [7,9,600,78394];
	print y;
	print y[2]+y[0];
	// z = y[0];
	// print z;
	var d = {'key':'value', 'my dictionary': 'my value'};
	print d;
	var this = {'key': 1};
	print this;
	print this['key'];
	d['key'];
	print d['my dictionary'];
	if (x % 5 == 0){
		print "yes, x mod 5 is zero";
	} else {
		print "no, x mod 5 is not zero";
	}
	for (var i = 0; i >= -5; i = i - 1) {
		print i;
	}
	while (x < 10){
		print x;
		x = x+1;
	}
}
