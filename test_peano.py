#!/usr/bin/env python3
"""
Comprehensive test cases for Peano arithmetic operations.
Tests all operations with various inputs, avoiding negative results.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from peano_app.peano import (
    int_to_peano_str, peano_str_to_int,
    successor, predecessor, add, multiply, subtract,
    less_than, equal, greater_than,
    div_peano, mod_peano, gcd_peano,
    make_fraction, add_fractions, subtract_fractions, 
    multiply_fractions, divide_fractions, simplify_fraction,
    start_trace, get_step_count, get_negative_flag
)

def test_conversion():
    """Test int <-> Peano string conversion"""
    print("=== CONVERSION TESTS ===")
    
    test_cases = [0, 1, 2, 3, 4, 5, 10, 15, 20]
    
    for n in test_cases:
        peano = int_to_peano_str(n)
        back = peano_str_to_int(peano)
        print(f"{n} -> {peano} -> {back} {'✓' if back == n else '✗'}")
    
    print()

def test_successor_predecessor():
    """Test successor and predecessor operations"""
    print("=== SUCCESSOR/PREDECESSOR TESTS ===")
    
    test_cases = [0, 1, 2, 3, 4, 5]
    
    for n in test_cases:
        peano_n = int_to_peano_str(n)
        
        # Test successor
        succ = successor(peano_n)
        succ_int = peano_str_to_int(succ)
        print(f"successor({n}) = {succ_int} {'✓' if succ_int == n + 1 else '✗'}")
        
        # Test predecessor (avoid negative)
        if n > 0:
            pred = predecessor(peano_n)
            pred_int = peano_str_to_int(pred)
            print(f"predecessor({n}) = {pred_int} {'✓' if pred_int == n - 1 else '✗'}")
        else:
            pred = predecessor(peano_n)
            pred_int = peano_str_to_int(pred)
            print(f"predecessor({n}) = {pred_int} (clamped) {'✓' if pred_int == 0 else '✗'}")
    
    print()

def test_addition():
    """Test addition operation"""
    print("=== ADDITION TESTS ===")
    
    test_cases = [
        (0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1),
        (2, 3), (3, 2), (4, 5), (5, 4), (0, 10), (10, 0),
        (7, 8), (12, 3), (6, 6)
    ]
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        result = add(peano_a, peano_b)
        result_int = peano_str_to_int(result)
        expected = a + b
        print(f"{a} + {b} = {result_int} {'✓' if result_int == expected else '✗'}")
    
    print()

def test_multiplication():
    """Test multiplication operation"""
    print("=== MULTIPLICATION TESTS ===")
    
    test_cases = [
        (0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1),
        (2, 3), (3, 2), (2, 4), (4, 2), (3, 3), (5, 2),
        (2, 5), (6, 1), (1, 7), (3, 4), (4, 3), (2, 6)
    ]
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        result = multiply(peano_a, peano_b)
        result_int = peano_str_to_int(result)
        expected = a * b
        print(f"{a} × {b} = {result_int} {'✓' if result_int == expected else '✗'}")
    
    print()

def test_subtraction():
    """Test subtraction operation (clamped at 0)"""
    print("=== SUBTRACTION TESTS ===")
    
    test_cases = [
        (0, 0), (1, 0), (1, 1), (2, 1), (3, 2), (5, 3),
        (10, 4), (7, 7), (8, 2), (6, 6),
        # Cases that would be negative (should clamp to 0)
        (0, 1), (1, 2), (2, 5), (3, 10)
    ]
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        result = subtract(peano_a, peano_b)
        result_int = peano_str_to_int(result)
        expected = max(0, a - b)  # Clamped subtraction
        status = "✓" if result_int == expected else "✗"
        if a < b:
            print(f"{a} - {b} = {result_int} (clamped) {status}")
        else:
            print(f"{a} - {b} = {result_int} {status}")
    
    print()

def test_comparisons():
    """Test comparison operations"""
    print("=== COMPARISON TESTS ===")
    
    test_cases = [
        (0, 0), (0, 1), (1, 0), (1, 1), (2, 3), (3, 2),
        (5, 5), (4, 7), (7, 4), (10, 2), (2, 10), (6, 6)
    ]
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        
        # Test less_than
        lt_result = less_than(peano_a, peano_b)
        lt_expected = a < b
        print(f"{a} < {b} = {lt_result} {'✓' if lt_result == lt_expected else '✗'}")
        
        # Test equal
        eq_result = equal(peano_a, peano_b)
        eq_expected = a == b
        print(f"{a} = {b} = {eq_result} {'✓' if eq_result == eq_expected else '✗'}")
        
        # Test greater_than
        gt_result = greater_than(peano_a, peano_b)
        gt_expected = a > b
        print(f"{a} > {b} = {gt_result} {'✓' if gt_result == gt_expected else '✗'}")
        
        print()

def test_division_modulo():
    """Test division and modulo operations"""
    print("=== DIVISION/MODULO TESTS ===")
    
    test_cases = [
        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
        (4, 2), (6, 2), (8, 2), (10, 2), (12, 2),
        (6, 3), (9, 3), (12, 3), (15, 3),
        (8, 4), (12, 4), (16, 4), (20, 4),
        (10, 5), (15, 5), (25, 5),
        (7, 3), (11, 4), (13, 5), (17, 6)  # With remainders
    ]
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        
        # Test division
        div_result = div_peano(peano_a, peano_b)
        div_int = peano_str_to_int(div_result)
        div_expected = a // b
        print(f"{a} ÷ {b} = {div_int} {'✓' if div_int == div_expected else '✗'}")
        
        # Test modulo
        mod_result = mod_peano(peano_a, peano_b)
        mod_int = peano_str_to_int(mod_result)
        mod_expected = a % b
        print(f"{a} mod {b} = {mod_int} {'✓' if mod_int == mod_expected else '✗'}")
        
        # Verify division property: a = b*q + r
        quotient = div_int
        remainder = mod_int
        check = b * quotient + remainder
        print(f"  Check: {b}×{quotient}+{remainder} = {check} {'✓' if check == a else '✗'}")
        print()

def test_gcd():
    """Test GCD operation"""
    print("=== GCD TESTS ===")
    
    test_cases = [
        (1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3),
        (4, 6), (6, 4), (8, 12), (12, 8), (15, 10), (10, 15),
        (7, 3), (9, 6), (14, 21), (18, 24), (25, 15),
        (13, 7), (16, 20), (21, 14), (30, 18)
    ]
    
    import math
    
    for a, b in test_cases:
        peano_a = int_to_peano_str(a)
        peano_b = int_to_peano_str(b)
        result = gcd_peano(peano_a, peano_b)
        result_int = peano_str_to_int(result)
        expected = math.gcd(a, b)
        print(f"gcd({a}, {b}) = {result_int} {'✓' if result_int == expected else '✗'}")
    
    print()

def test_fractions():
    """Test fraction operations"""
    print("=== FRACTION TESTS ===")
    
    # Test fraction creation and simplification
    test_fractions = [
        (1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (4, 6), (6, 4),
        (8, 12), (12, 8), (15, 10), (10, 15), (9, 6), (6, 9)
    ]
    
    print("--- Fraction Simplification ---")
    for num, den in test_fractions:
        peano_num = int_to_peano_str(num)
        peano_den = int_to_peano_str(den)
        frac = make_fraction(peano_num, peano_den)
        simplified = simplify_fraction(frac)
        
        simp_num = peano_str_to_int(simplified.numerator)
        simp_den = peano_str_to_int(simplified.denominator)
        
        import math
        gcd_val = math.gcd(num, den)
        expected_num = num // gcd_val
        expected_den = den // gcd_val
        
        correct = simp_num == expected_num and simp_den == expected_den
        print(f"{num}/{den} -> {simp_num}/{simp_den} {'✓' if correct else '✗'}")
    
    print("\n--- Fraction Addition ---")
    addition_cases = [
        ((1, 2), (1, 3)), ((1, 4), (1, 4)), ((2, 3), (1, 6)),
        ((3, 4), (1, 8)), ((1, 2), (1, 2)), ((2, 5), (3, 10))
    ]
    
    for (a_num, a_den), (b_num, b_den) in addition_cases:
        frac_a = make_fraction(int_to_peano_str(a_num), int_to_peano_str(a_den))
        frac_b = make_fraction(int_to_peano_str(b_num), int_to_peano_str(b_den))
        
        result = add_fractions(frac_a, frac_b)
        res_num = peano_str_to_int(result.numerator)
        res_den = peano_str_to_int(result.denominator)
        
        # Calculate expected result
        expected_num = a_num * b_den + b_num * a_den
        expected_den = a_den * b_den
        import math
        gcd_val = math.gcd(expected_num, expected_den)
        expected_num //= gcd_val
        expected_den //= gcd_val
        
        correct = res_num == expected_num and res_den == expected_den
        print(f"{a_num}/{a_den} + {b_num}/{b_den} = {res_num}/{res_den} {'✓' if correct else '✗'}")
    
    print("\n--- Fraction Subtraction ---")
    subtraction_cases = [
        ((3, 4), (1, 4)), ((1, 2), (1, 3)), ((5, 6), (1, 3)),
        ((7, 8), (3, 8)), ((2, 3), (1, 6)), ((4, 5), (2, 10))
    ]
    
    for (a_num, a_den), (b_num, b_den) in subtraction_cases:
        # Only test cases where a >= b to avoid negatives
        if a_num * b_den >= b_num * a_den:
            frac_a = make_fraction(int_to_peano_str(a_num), int_to_peano_str(a_den))
            frac_b = make_fraction(int_to_peano_str(b_num), int_to_peano_str(b_den))
            
            result = subtract_fractions(frac_a, frac_b)
            res_num = peano_str_to_int(result.numerator)
            res_den = peano_str_to_int(result.denominator)
            
            # Calculate expected result
            expected_num = a_num * b_den - b_num * a_den
            expected_den = a_den * b_den
            import math
            if expected_num > 0:
                gcd_val = math.gcd(expected_num, expected_den)
                expected_num //= gcd_val
                expected_den //= gcd_val
            else:
                expected_num = 0
                expected_den = 1
            
            correct = res_num == expected_num and res_den == expected_den
            print(f"{a_num}/{a_den} - {b_num}/{b_den} = {res_num}/{res_den} {'✓' if correct else '✗'}")

    print("\n--- Fraction Multiplication ---")
    mult_cases = [
        ((1, 2), (1, 3)), ((2, 3), (3, 4)), ((1, 4), (4, 1)),
        ((3, 5), (2, 7)), ((6, 8), (4, 9))
    ]
    
    for (a_num, a_den), (b_num, b_den) in mult_cases:
        frac_a = make_fraction(int_to_peano_str(a_num), int_to_peano_str(a_den))
        frac_b = make_fraction(int_to_peano_str(b_num), int_to_peano_str(b_den))
        
        result = multiply_fractions(frac_a, frac_b)
        res_num = peano_str_to_int(result.numerator)
        res_den = peano_str_to_int(result.denominator)
        
        # Calculate expected result
        expected_num = a_num * b_num
        expected_den = a_den * b_den
        import math
        gcd_val = math.gcd(expected_num, expected_den)
        expected_num //= gcd_val
        expected_den //= gcd_val
        
        correct = res_num == expected_num and res_den == expected_den
        print(f"{a_num}/{a_den} × {b_num}/{b_den} = {res_num}/{res_den} {'✓' if correct else '✗'}")

    print("\n--- Fraction Division ---")
    division_cases = [
        ((1, 2), (1, 3)), ((2, 3), (1, 4)), ((3, 4), (3, 8)),
        ((6, 8), (2, 4)), ((4, 5), (2, 5)), ((9, 12), (3, 4))
    ]
    
    for (a_num, a_den), (b_num, b_den) in division_cases:
        frac_a = make_fraction(int_to_peano_str(a_num), int_to_peano_str(a_den))
        frac_b = make_fraction(int_to_peano_str(b_num), int_to_peano_str(b_den))
        
        result = divide_fractions(frac_a, frac_b)
        res_num = peano_str_to_int(result.numerator)
        res_den = peano_str_to_int(result.denominator)
        
        # Calculate expected result: (a/b) ÷ (c/d) = (a/b) × (d/c) = (a×d)/(b×c)
        expected_num = a_num * b_den
        expected_den = a_den * b_num
        import math
        gcd_val = math.gcd(expected_num, expected_den)
        expected_num //= gcd_val
        expected_den //= gcd_val
        
        correct = res_num == expected_num and res_den == expected_den
        print(f"{a_num}/{a_den} ÷ {b_num}/{b_den} = {res_num}/{res_den} {'✓' if correct else '✗'}")
    
    print()

def test_step_counting():
    """Test step counting functionality"""
    print("=== STEP COUNTING TESTS ===")
    
    operations = [
        ("2 + 3", lambda: add(int_to_peano_str(2), int_to_peano_str(3))),
        ("3 × 4", lambda: multiply(int_to_peano_str(3), int_to_peano_str(4))),
        ("10 ÷ 3", lambda: div_peano(int_to_peano_str(10), int_to_peano_str(3))),
        ("gcd(12, 8)", lambda: gcd_peano(int_to_peano_str(12), int_to_peano_str(8)))
    ]
    
    for desc, op in operations:
        start_trace()
        result = op()
        steps = get_step_count()
        negative = get_negative_flag()
        result_int = peano_str_to_int(result) if isinstance(result, str) else result
        print(f"{desc} = {result_int}, steps: {steps}, negative encountered: {negative}")
    
    print()

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("=== EDGE CASE TESTS ===")
    
    # Zero operations
    print("--- Zero Operations ---")
    zero = int_to_peano_str(0)
    one = int_to_peano_str(1)
    five = int_to_peano_str(5)
    
    print(f"0 + 0 = {peano_str_to_int(add(zero, zero))}")
    print(f"0 × 5 = {peano_str_to_int(multiply(zero, five))}")
    print(f"5 × 0 = {peano_str_to_int(multiply(five, zero))}")
    print(f"0 ÷ 1 = {peano_str_to_int(div_peano(zero, one))}")
    print(f"0 mod 5 = {peano_str_to_int(mod_peano(zero, five))}")
    
    # Identity operations
    print("\n--- Identity Operations ---")
    print(f"5 + 0 = {peano_str_to_int(add(five, zero))}")
    print(f"5 × 1 = {peano_str_to_int(multiply(five, one))}")
    print(f"5 ÷ 1 = {peano_str_to_int(div_peano(five, one))}")
    print(f"5 ÷ 5 = {peano_str_to_int(div_peano(five, five))}")
    
    # Clamping tests
    print("\n--- Clamping Tests ---")
    print(f"0 - 1 = {peano_str_to_int(subtract(zero, one))} (should be 0)")
    print(f"2 - 5 = {peano_str_to_int(subtract(int_to_peano_str(2), five))} (should be 0)")
    
    print()

def run_all_tests():
    """Run all test suites"""
    print("🧮 COMPREHENSIVE PEANO ARITHMETIC TESTS 🧮\n")
    
    test_conversion()
    test_successor_predecessor()
    test_addition()
    test_multiplication()
    test_subtraction()
    test_comparisons()
    test_division_modulo()
    test_gcd()
    test_fractions()
    test_step_counting()
    test_edge_cases()
    
    print("🎉 ALL TESTS COMPLETED! 🎉")

if __name__ == "__main__":
    run_all_tests()