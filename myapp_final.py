#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学四则运算题目生成器
"""

import argparse
import random
import sys
from fractions import Fraction

class MathExerciseGenerator:
    def __init__(self, max_range):
        self.max_range = max_range
        self.generated = set()
    
    def generate_number(self):
        """生成数字（自然数或真分数）"""
        if random.choice([True, False]):
            # 自然数
            return random.randint(1, self.max_range - 1)
        else:
            # 真分数
            denominator = random.randint(2, self.max_range - 1)
            numerator = random.randint(1, denominator - 1)
            return Fraction(numerator, denominator)
    
    def format_number(self, num):
        """格式化数字输出"""
        if isinstance(num, int):
            return str(num)
        elif isinstance(num, Fraction):
            if num.denominator == 1:
                return str(num.numerator)
            elif num >= 1:
                # 带分数
                whole = num.numerator // num.denominator
                remainder = num.numerator % num.denominator
                if remainder == 0:
                    return str(whole)
                return f"{whole}'{remainder}/{num.denominator}"
            else:
                # 真分数
                return f"{num.numerator}/{num.denominator}"
        else:
            return str(num)
    
    def generate_exercise(self):
        """生成一道题目"""
        operators = ['+', '-', '×', '÷']
        op_count = random.randint(1, 3)
        
        # 生成简单的两数运算
        if op_count == 1:
            num1 = self.generate_number()
            num2 = self.generate_number()
            op = random.choice(operators)
            
            # 确保减法不产生负数
            if op == '-':
                if isinstance(num1, (int, Fraction)) and isinstance(num2, (int, Fraction)):
                    if Fraction(num1) < Fraction(num2):
                        num1, num2 = num2, num1
            
            # 确保除法分母不为0
            if op == '÷' and num2 == 0:
                num2 = 1
            
            expr = f"{self.format_number(num1)} {op} {self.format_number(num2)}"
            
            # 计算结果
            f1, f2 = Fraction(num1), Fraction(num2)
            if op == '+':
                result = f1 + f2
            elif op == '-':
                result = f1 - f2
            elif op == '×':
                result = f1 * f2
            elif op == '÷':
                result = f1 / f2
            
            return expr, result
        
        # 更复杂的表达式（支持括号）
        else:
            num1 = self.generate_number()
            num2 = self.generate_number()
            num3 = self.generate_number()
            
            op1 = random.choice(['+', '-', '×', '÷'])
            op2 = random.choice(['+', '-', '×', '÷'])
            
            f1, f2, f3 = Fraction(num1), Fraction(num2), Fraction(num3)
            
            # 确保减法不产生负数和除法分母不为0
            if op1 == '-' and f1 < f2:
                num1, num2 = num2, num1
                f1, f2 = f2, f1
            if op1 == '÷' and f2 == 0:
                num2 = 1
                f2 = Fraction(1)
            if op2 == '÷' and f3 == 0:
                num3 = 1
                f3 = Fraction(1)
            
            # 决定是否使用括号
            use_parentheses = random.choice([True, False])
            
            if use_parentheses:
                # 随机选择括号位置：(a op1 b) op2 c 或 a op1 (b op2 c)
                parentheses_position = random.choice(['left', 'right'])
                
                if parentheses_position == 'left':
                    # (a op1 b) op2 c
                    expr = f"({self.format_number(num1)} {op1} {self.format_number(num2)}) {op2} {self.format_number(num3)}"
                    
                    # 计算括号内的结果
                    if op1 == '+':
                        bracket_result = f1 + f2
                    elif op1 == '-':
                        bracket_result = f1 - f2
                    elif op1 == '×':
                        bracket_result = f1 * f2
                    else:  # op1 == '÷'
                        bracket_result = f1 / f2
                    
                    # 计算最终结果
                    if op2 == '+':
                        result = bracket_result + f3
                    elif op2 == '-':
                        result = bracket_result - f3
                        # 确保结果不为负数
                        if result < 0:
                            result = f3 - bracket_result
                            expr = f"{self.format_number(num3)} - ({self.format_number(num1)} {op1} {self.format_number(num2)})"
                    elif op2 == '×':
                        result = bracket_result * f3
                    else:  # op2 == '÷'
                        result = bracket_result / f3
                
                else:  # parentheses_position == 'right'
                    # a op1 (b op2 c)
                    expr = f"{self.format_number(num1)} {op1} ({self.format_number(num2)} {op2} {self.format_number(num3)})"
                    
                    # 计算括号内的结果
                    if op2 == '+':
                        bracket_result = f2 + f3
                    elif op2 == '-':
                        bracket_result = f2 - f3
                        # 确保括号内不为负数
                        if bracket_result < 0:
                            bracket_result = f3 - f2
                            expr = f"{self.format_number(num1)} {op1} ({self.format_number(num3)} - {self.format_number(num2)})"
                    elif op2 == '×':
                        bracket_result = f2 * f3
                    else:  # op2 == '÷'
                        bracket_result = f2 / f3
                    
                    # 计算最终结果
                    if op1 == '+':
                        result = f1 + bracket_result
                    elif op1 == '-':
                        result = f1 - bracket_result
                        # 确保结果不为负数
                        if result < 0:
                            result = bracket_result - f1
                            expr = f"({self.format_number(num2)} {op2} {self.format_number(num3)}) - {self.format_number(num1)}"
                    elif op1 == '×':
                        result = f1 * bracket_result
                    else:  # op1 == '÷'
                        result = f1 / bracket_result
            
            else:
                # 不使用括号，按运算优先级计算
                expr = f"{self.format_number(num1)} {op1} {self.format_number(num2)} {op2} {self.format_number(num3)}"
                
                # 检查运算优先级：乘除法优先于加减法
                if op2 in ['×', '÷'] and op1 in ['+', '-']:
                    # 先计算右边的乘除法
                    if op2 == '×':
                        temp = f2 * f3
                    else:  # op2 == '÷'
                        temp = f2 / f3
                    
                    # 再计算左边的加减法
                    if op1 == '+':
                        result = f1 + temp
                    else:  # op1 == '-'
                        result = f1 - temp
                        # 确保结果不为负数
                        if result < 0:
                            result = temp - f1
                            expr = f"{self.format_number(num2)} {op2} {self.format_number(num3)} - {self.format_number(num1)}"
                elif op1 in ['×', '÷'] and op2 in ['+', '-']:
                    # 先计算左边的乘除法
                    if op1 == '×':
                        temp = f1 * f2
                    else:  # op1 == '÷'
                        temp = f1 / f2
                    
                    # 再计算右边的加减法
                    if op2 == '+':
                        result = temp + f3
                    else:  # op2 == '-'
                        result = temp - f3
                        # 确保结果不为负数
                        if result < 0:
                            result = f3 - temp
                            expr = f"{self.format_number(num3)} - {self.format_number(num1)} {op1} {self.format_number(num2)}"
                else:
                    # 按从左到右的顺序计算（同优先级）
                    if op1 == '+':
                        temp = f1 + f2
                    elif op1 == '-':
                        temp = f1 - f2
                    elif op1 == '×':
                        temp = f1 * f2
                    else:  # op1 == '÷'
                        temp = f1 / f2
                    
                    if op2 == '+':
                        result = temp + f3
                    elif op2 == '-':
                        result = temp - f3
                        # 确保结果不为负数
                        if result < 0:
                            result = f3 - temp
                            result = abs(result)
                    elif op2 == '×':
                        result = temp * f3
                    else:  # op2 == '÷'
                        result = temp / f3
            
            return expr, result
    
    def generate_exercises(self, count):
        """生成指定数量的题目"""
        exercises = []
        attempts = 0
        max_attempts = count * 10
        
        while len(exercises) < count and attempts < max_attempts:
            try:
                expr, result = self.generate_exercise()
                
                # 简单的重复检查
                if expr not in self.generated:
                    self.generated.add(expr)
                    exercises.append((expr, result))
                
                attempts += 1
            except:
                attempts += 1
                continue
        
        return exercises

def parse_fraction(s):
    """解析分数字符串"""
    s = s.strip()
    if "'" in s:
        # 带分数格式 2'3/8
        parts = s.split("'")
        whole = int(parts[0])
        frac_part = parts[1].split("/")
        numerator = int(frac_part[0])
        denominator = int(frac_part[1])
        return Fraction(whole * denominator + numerator, denominator)
    elif "/" in s:
        # 真分数格式 3/5
        parts = s.split("/")
        return Fraction(int(parts[0]), int(parts[1]))
    else:
        # 自然数
        return Fraction(int(s))

def evaluate_expression(expr):
    """计算表达式的值，支持括号"""
    expr = expr.strip()
    
    # 替换运算符
    expr = expr.replace('×', '*').replace('÷', '/')
    
    # 处理括号
    if '(' in expr and ')' in expr:
        return evaluate_with_parentheses(expr)
    else:
        return evaluate_without_parentheses(expr)

def evaluate_with_parentheses(expr):
    """处理带括号的表达式"""
    # 找到括号的位置
    start = expr.find('(')
    end = expr.find(')')
    
    if start == -1 or end == -1:
        return evaluate_without_parentheses(expr)
    
    # 提取括号内的表达式
    bracket_expr = expr[start+1:end]
    bracket_result = evaluate_without_parentheses(bracket_expr)
    
    # 构造新的表达式，用括号的结果替换括号部分
    # 需要处理分数格式
    generator = MathExerciseGenerator(10)
    bracket_result_str = generator.format_number(bracket_result)
    
    new_expr = expr[:start] + bracket_result_str + expr[end+1:]
    
    # 递归计算剩余表达式
    return evaluate_without_parentheses(new_expr.strip())

def evaluate_without_parentheses(expr):
    """处理不带括号的表达式"""
    expr = expr.strip()
    tokens = expr.split()
    
    if len(tokens) == 1:
        # 单个数字
        return parse_fraction(tokens[0])
    elif len(tokens) == 3:
        # 简单的二元运算
        left = parse_fraction(tokens[0])
        op = tokens[1]
        right = parse_fraction(tokens[2])
        
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
    
    elif len(tokens) == 5:
        # 三元运算（考虑运算优先级）
        left = parse_fraction(tokens[0])
        op1 = tokens[1]
        middle = parse_fraction(tokens[2])
        op2 = tokens[3]
        right = parse_fraction(tokens[4])
        
        # 检查运算优先级：乘除法优先于加减法
        if op2 in ['*', '/'] and op1 in ['+', '-']:
            # 先计算右边的乘除法
            if op2 == '*':
                temp = middle * right
            else:  # op2 == '/'
                temp = middle / right
            
            # 再计算左边的加减法
            if op1 == '+':
                return left + temp
            else:  # op1 == '-'
                return left - temp
        else:
            # 按从左到右的顺序计算
            if op1 == '+':
                temp = left + middle
            elif op1 == '-':
                temp = left - middle
            elif op1 == '*':
                temp = left * middle
            elif op1 == '/':
                temp = left / middle
            
            # 再计算右边
            if op2 == '+':
                return temp + right
            elif op2 == '-':
                return temp - right
            elif op2 == '*':
                return temp * right
            elif op2 == '/':
                return temp / right
    
    return Fraction(0)

def check_answers(exercise_file, answer_file):
    """检查答案正确性"""
    try:
        # 读取题目
        with open(exercise_file, 'r', encoding='utf-8') as f:
            exercises = f.readlines()
        
        # 读取用户答案
        with open(answer_file, 'r', encoding='utf-8') as f:
            user_answers = f.readlines()
        
        correct = []
        wrong = []
        
        for i, (exercise_line, answer_line) in enumerate(zip(exercises, user_answers), 1):
            # 解析题目
            exercise = exercise_line.strip()
            user_answer = answer_line.strip()
            
            # 提取表达式部分
            if '. ' in exercise:
                expr_part = exercise.split('. ', 1)[1].replace(' =', '')
            else:
                expr_part = exercise.replace(' =', '')
            
            # 提取用户答案
            if '. ' in user_answer:
                answer_part = user_answer.split('. ', 1)[1]
            else:
                answer_part = user_answer
            
            try:
                # 计算正确答案
                correct_answer = evaluate_expression(expr_part)
                generator = MathExerciseGenerator(10)
                correct_answer_str = generator.format_number(correct_answer)
                
                # 比较答案
                if answer_part.strip() == correct_answer_str:
                    correct.append(i)
                else:
                    wrong.append(i)
            except:
                wrong.append(i)
        
        return {'correct': correct, 'wrong': wrong}
    
    except Exception as e:
        print(f"检查答案时出错：{e}")
        return {'correct': [], 'wrong': []}

def save_grade(result, grade_file='Grade.txt'):
    """保存评分结果"""
    with open(grade_file, 'w', encoding='utf-8') as f:
        correct_count = len(result['correct'])
        wrong_count = len(result['wrong'])
        
        correct_nums = ', '.join(map(str, result['correct'])) if result['correct'] else ''
        wrong_nums = ', '.join(map(str, result['wrong'])) if result['wrong'] else ''
        
        f.write(f"Correct: {correct_count} ({correct_nums})\n")
        f.write(f"Wrong: {wrong_count} ({wrong_nums})\n")

def main():
    parser = argparse.ArgumentParser(description='小学四则运算题目生成器')
    
    # 生成题目参数
    parser.add_argument('-n', type=int, help='生成题目的个数')
    parser.add_argument('-r', type=int, help='数值范围（必须指定）')
    
    # 检查答案参数
    parser.add_argument('-e', type=str, help='题目文件路径')
    parser.add_argument('-a', type=str, help='答案文件路径')
    
    args = parser.parse_args()
    
    if args.n is not None:
        # 生成题目模式
        if args.r is None:
            print("错误：必须使用 -r 参数指定数值范围")
            parser.print_help()
            return
        
        if args.r < 1:
            print("错误：-r 参数必须为1或其他自然数")
            return
        
        print(f"正在生成 {args.n} 道题目，数值范围为 {args.r}...")
        
        generator = MathExerciseGenerator(args.r)
        exercises = generator.generate_exercises(args.n)
        
        # 保存题目
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, (expr, _) in enumerate(exercises, 1):
                f.write(f"{i}. {expr} =\n")
        
        # 保存答案
        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for i, (_, result) in enumerate(exercises, 1):
                answer = generator.format_number(result)
                f.write(f"{i}. {answer}\n")
        
        print(f"成功生成 {len(exercises)} 道题目")
        print("题目已保存到 Exercises.txt")
        print("答案已保存到 Answers.txt")
    
    elif args.e and args.a:
        # 检查答案模式
        print(f"正在检查答案...")
        print(f"题目文件：{args.e}")
        print(f"答案文件：{args.a}")
        
        result = check_answers(args.e, args.a)
        save_grade(result)
        
        correct_count = len(result['correct'])
        wrong_count = len(result['wrong'])
        total = correct_count + wrong_count
        
        print(f"检查完成！")
        print(f"总题目数：{total}")
        print(f"正确：{correct_count} 题")
        print(f"错误：{wrong_count} 题")
        print("详细结果已保存到 Grade.txt")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()