""" Módulo de entrada do projeto """


from pycharmers.engine import DisplayManager


def main():
    """ Função principal """

    display = DisplayManager((320, 240), scale=2)

    # Loop principal do jogo
    while True:
        display.tick()
        display.draw([])


# Chamar a função main ao rodar o módulo
if __name__ == "__main__":
    main()
