from spherepop import parse_operation, parse_sphere, render_expr

if __name__ == "__main__":
    sigma = parse_sphere("(A (B C) D)")
    op = parse_operation("POP 1")
    print("sigma:", render_expr(sigma))
    print("operation:", op)
