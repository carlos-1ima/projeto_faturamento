def eh_venda(cfop):
    if not cfop:
        return False
    return str(cfop).startswith(("5", "6", "7"))