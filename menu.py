def menu():
    layar.blit(pygame.transform.scale(background_img,(500,700)),(0,0))
    draw_text(layar, "WATCHOUT!", 70, WIDTH/2, HEIGHT/4)
    draw_text(layar, "Menu", 20, WIDTH/2, HEIGHT/2)
    draw_text(layar, "Press any key to play", 22, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOSEBUTTONDOWN:
                waiting = False
                waiting_screen()