#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试流程
1. 生成指定数量的题目
2. 生成测试答案（包含正确和错误答案）
3. 检查答案并生成评分
"""

import subprocess
import sys
import argparse

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def full_test_workflow(num_questions, value_range, correct_ratio=0.6):
    """完整的测试工作流程"""
    print("=" * 50)
    print("小学四则运算题目生成器 - 完整测试流程")
    print("=" * 50)
    
    # 步骤1: 生成题目
    print(f"\n步骤1: 生成 {num_questions} 道题目 (范围: {value_range})")
    cmd1 = f"py myapp_final.py -n {num_questions} -r {value_range}"
    success, stdout, stderr = run_command(cmd1)
    
    if success:
        print("✓ 题目生成成功")
        print(stdout.strip())
    else:
        print("✗ 题目生成失败")
        print(stderr)
        return
    
    # 步骤2: 生成测试答案
    print(f"\n步骤2: 生成测试答案 (正确率: {correct_ratio*100}%)")
    cmd2 = f"py generate_test_answers.py -e Exercises.txt -o TestAnswers.txt -r {correct_ratio}"
    success, stdout, stderr = run_command(cmd2)
    
    if success:
        print("✓ 测试答案生成成功")
        print(stdout.strip())
    else:
        print("✗ 测试答案生成失败")
        print(stderr)
        return
    
    # 步骤3: 检查答案
    print(f"\n步骤3: 检查答案")
    cmd3 = f"py myapp_final.py -e Exercises.txt -a TestAnswers.txt"
    success, stdout, stderr = run_command(cmd3)
    
    if success:
        print("✓ 答案检查完成")
        print(stdout.strip())
    else:
        print("✗ 答案检查失败")
        print(stderr)
        return
    
    # 显示结果文件
    print(f"\n步骤4: 查看结果")
    try:
        print("\n--- 生成的题目 (前5道) ---")
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(line.strip())
        
        print(f"\n--- 标准答案 (前5个) ---")
        with open('Answers.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(line.strip())
        
        print(f"\n--- 测试答案 (前5个) ---")
        with open('TestAnswers.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(line.strip())
        
        print(f"\n--- 评分结果 ---")
        with open('Grade.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content.strip())
        
    except Exception as e:
        print(f"读取结果文件时出错: {e}")
    
    print(f"\n=" * 50)
    print("测试完成！生成的文件:")
    print("- Exercises.txt: 题目文件")
    print("- Answers.txt: 标准答案文件")
    print("- TestAnswers.txt: 测试答案文件")
    print("- Grade.txt: 评分结果文件")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='完整测试流程')
    parser.add_argument('-n', '--num', type=int, default=10, help='题目数量 (默认: 10)')
    parser.add_argument('-r', '--range', type=int, default=10, help='数值范围 (默认: 10)')
    parser.add_argument('-c', '--correct', type=float, default=0.6, help='正确答案比例 (默认: 0.6)')
    
    args = parser.parse_args()
    
    if args.range < 1:
        print("错误: 数值范围必须大于等于1")
        return
    
    if not (0.0 <= args.correct <= 1.0):
        print("错误: 正确答案比例必须在 0.0 到 1.0 之间")
        return
    
    full_test_workflow(args.num, args.range, args.correct)

if __name__ == "__main__":
    main()