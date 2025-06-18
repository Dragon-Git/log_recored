import re
import json

def parse_uvm_log(log_file_path):
    trace_events = []
    with open(log_file_path, "r") as f:
        for line in f:
            line = line.strip()
            # 正则匹配新格式的 UVM 日志行，提取 component path（reporter）
            match = re.match(
                r"^(UVM_\w+) ([^(]*)\((\d+)\) @ (\d+): ([^\ ]+) \[(.*)\] (.*)$",
                line
            )
            if not match:
                print(f"Ignoring line: {line}")
                continue
            print(f"Line: {line}")
            print(f"Match: {match.groups()}")

            cat, file_path, line_number, ts, pid, tid, message = match.groups()
            ts = ts  # 假设时间戳单位为纳秒，转换为微秒（若需）

            # 构造 src_href（vscode 协议）
            src_href = f"vscode://{file_path}#{line_number}"

            # 构造事件对象，新增 reporter 字段
            event = {
                "pid": pid,
                "tid": tid,
                "ts": ts,
                "ph": "i",  # 瞬时事件
                "name": f"{tid} Event(uvm message ID)", 
                "cat": cat,
                "args": {
                    "message": message,
                    "src_href": src_href,
                }
            }
            trace_events.append(event)

    # 构造最终 JSON 结构
    return {
        "traceEvents": trace_events
    }

def main():
    log_file = "uvm.log"  # 替换为你的 UVM 日志文件路径
    output_file = "uvm_log.json"

    trace_data = parse_uvm_log(log_file)
    with open(output_file, "w") as f:
        json.dump(trace_data, f, indent=2)

    print(f"Trace events saved to {output_file}")

if __name__ == "__main__":
    main()