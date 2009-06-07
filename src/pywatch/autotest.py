if __name__ == "__main__":
    import watcher

    files = ("tests.py", "watcher.py")
    cmds = ("python tests.py", )

    w = watcher.Watcher(files, cmds, verbose=True)

    w.run_monitor()
