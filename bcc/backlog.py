#!/usr/bin/env python

from bcc import BPF
import ctypes as ct

bcc_prog = """
#define KBUILD_MODNAME "backlog"
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

void print_stats(struct pt_regs *ctx, struct sock *sk, struct sk_buff *skb,
                          struct request_sock *req,
                          bool fastopen)
{
        u16 lport = sk->__sk_common.skc_num;
        bpf_trace_printk("port: %d, backlog: %d, max_backlog: %d\\n",
                         lport,
                         sk->sk_ack_backlog,
                         sk->sk_max_ack_backlog);
}
"""

b = BPF(text=bcc_prog)
b.attach_kprobe(event="tcp_check_req", fn_name="print_stats")
b.trace_print()
