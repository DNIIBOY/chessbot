from CLI import CLI


def main():
    cli = CLI()
    cli.setup()
    try:
        cli.show_home_page()
    except KeyboardInterrupt:
        cli.quit()


if __name__ == '__main__':
    main()
