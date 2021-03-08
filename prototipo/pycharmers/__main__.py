""" Módulo de entrada do projeto """


from pycharmers.engine import DisplayManager, InputManager
from pycharmers.settings import mappings


def main():
    """ Função principal """

    display = DisplayManager((320, 240), scale=2)
    inputs = InputManager(mappings)

    # Loop principal do jogo
    while True:
        display.tick()
        inputs.update()
        display.draw([])


# Chamar a função main ao rodar o módulo
if __name__ == "__main__":
    main()
