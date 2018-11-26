#include <stdio.h>
#include <stdlib.h>

#define ROR(x,n) (((x)<<(n)) | ((x) >> (32 - (n))))

unsigned long password(unsigned long seed, unsigned char last_mac_octet)
{
	unsigned long b = seed & 0x00FFFFFF;
	unsigned long r = ROR(b + 0x10F0A563, last_mac_octet & 7);
	return r^b;
}

int main(int argc, char **argv)
{
	int last_byte, passwd;

	if (argc != 2) {
		printf ("Use: %s <first MAC address value -- see ATSH result>\n", argv[0]);
		printf ("Sample: %s aa:bb:cc:dd:ee:ff\n", argv[0]);
		exit(0);
	}

	sscanf(argv[1], "%*02x:%*02x:%*02x:%*02x:%*02x:%02x", &last_byte);
	passwd = password(0, last_byte);

	//printf("Password: %08X\n", password(0, last_byte));
	printf("To enable DebugFlag:\n    ZHAL> ATEN 1,%08X\n\n", passwd);	
	printf("To disable DebugFlag:\n    ZHAL> ATEN 0,%08X\n\n", passwd);	
	return 0;
}



