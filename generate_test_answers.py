#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试答案生成器
根据题目文件生成随机的测试答案（包含正确和错误答案）
"""

import random
import argparse
from fractions import Fraction
from myapp_final import MathExerciseGenerator, evaluate_expression, parse_fraction

def generate_random_answer(generator):
    """生成一个随机答案"""
    answer_type = random.choice(['correct', 'wrong_number', 'wrong_fraction', 'zero'])
    
    if answer_type == 'correct':
        # 这个会在主函数中被正确答案替换
        return "CORRECT_PLACEHOLDER"
    elif answer_type == 'wrong_number':
        # 生成错误的整数答案
        return str(random.randint(0, 20))
    elif answer_type == 'wrong_fraction':
        # 生成错误的分数答案
        num = random.randint(1, 10)
        den = random.randint(2, 10)
        return f"{num}/{den}"
    else:
        # 返回0作为错误答案
        return "0"

def generate_test_answers(exercise_file, output_file, correct_ratio=0.6):
    """
    生成测试答案文件
    correct_ratio: 正确答案的比例（0.0-1.0）
    """
    try:
        # 读取题目文件
        with open(exercise_file, 'r', encoding='utf-8') as f:
            exercises = f.readlines()
        
        generator = MathExerciseGenerator(10)
        test_answers = []
        
        total_questions = len(exercises)
        correct_count = int(total_questions * correct_ratio)
        
        # 决定哪些题目给正确答案
        correct_indices = set(random.sample(range(total_questions), correct_count))
        
        print(f"总题目数: {total_questions}")
        print(f"正确答案数: {correct_count}")
        print(f"错误答案数: {total_questions - correct_count}")
        print(f"正确答案题号: {sorted(list(correct_indices))}")
        
        for i, exercise_line in enumerate(exercises):
            exercise = exercise_line.strip()
            
            # 提取表达式部分
            if '. ' in exercise:
                expr_part = exercise.split('. ', 1)[1].replace(' =', '')
            else:
                expr_part = exercise.replace(' =', '')
            
            if i in correct_indices:
                # 生成正确答案
                try:
                    correct_answer = evaluate_expression(expr_part)
                    answer = generator.format_number(correct_answer)
                except:
                    answer = "0"
            else:
                # 生成错误答案
                try:
                    # 先计算正确答案，然后生成一个不同的错误答案
                    correct_answer = evaluate_expression(expr_part)
                    correct_str = generator.format_number(correct_answer)
                    
                    # 生成错误答案，确保与正确答案不同
                    for _ in range(10):  # 最多尝试10次
                        wrong_answer = generate_random_answer(generator)
                        if wrong_answer != correct_str and wrong_answer != "CORRECT_PLACEHOLDER":
                            answer = wrong_answer
                            break
                    else:
                        answer = "0"  # 如果都不行，就用0
                except:
                    answer = "0"
            
            test_answers.append(f"{i+1}. {answer}")
        
        # 保存测试答案文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for answer in test_answers:
                f.write(f"{answer}\n")
        
        print(f"测试答案已保存到: {output_file}")
        return correct_indices
        
    except Exception as e:
        print(f"生成测试答案时出错: {e}")
        return set()

def main():
    parser = argparse.ArgumentParser(description='测试答案生成器')
    parser.add_argument('-e', '--exercise', required=True, help='题目文件路径')
    parser.add_argument('-o', '--output', default='TestAnswers.txt', help='输出的测试答案文件')
    parser.add_argument('-r', '--ratio', type=float, default=0.6, help='正确答案比例 (0.0-1.0)')
    
    args = parser.parse_args()
    
    if not (0.0 <= args.ratio <= 1.0):
        print("错误: 正确答案比例必须在 0.0 到 1.0 之间")
        return
    
    print(f"正在为 {args.exercise} 生成测试答案...")
    print(f"正确答案比例: {args.ratio}")
    
    correct_indices = generate_test_answers(args.exercise, args.output, args.ratio)
    
    if correct_indices:
        print(f"成功生成测试答案文件: {args.output}")
        print("你现在可以使用以下命令检查答案:")
        print(f"py myapp_final.py -e {args.exercise} -a {args.output}")

if __name__ == "__main__":
    main()