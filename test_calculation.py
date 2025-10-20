#!/usr/bin/env python3
"""
测试计算修复
"""

from myapp_final import evaluate_expression, MathExerciseGenerator

def test_calculations():
    generator = MathExerciseGenerator(10)
    
    # 测试第1题：5/6 + 3/4 × 1/4
    expr1 = "5/6 + 3/4 × 1/4"
    result1 = evaluate_expression(expr1)
    formatted1 = generator.format_number(result1)
    print(f"第1题: {expr1} = {formatted1}")
    print(f"计算过程: 3/4 × 1/4 = 3/16, 5/6 + 3/16 = 40/48 + 9/48 = 49/48 = 1'1/48")
    
    # 测试第12题：4/7 + 8 × 1/3
    expr12 = "4/7 + 8 × 1/3"
    result12 = evaluate_expression(expr12)
    formatted12 = generator.format_number(result12)
    print(f"\n第12题: {expr12} = {formatted12}")
    print(f"计算过程: 8 × 1/3 = 8/3, 4/7 + 8/3 = 12/21 + 56/21 = 68/21 = 3'5/21")
    
    # 测试其他运算优先级
    test_cases = [
        "1 + 2 × 3",  # 应该是 7
        "6 ÷ 2 + 1",  # 应该是 4
        "2 × 3 + 4",  # 应该是 10
        "1/2 + 1/4 × 2",  # 应该是 1
    ]
    
    print(f"\n其他测试:")
    for expr in test_cases:
        result = evaluate_expression(expr)
        formatted = generator.format_number(result)
        print(f"{expr} = {formatted}")

if __name__ == "__main__":
    test_calculations()