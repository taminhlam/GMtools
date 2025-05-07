local utf8 = require("utf8")

function love.load()
  -- enable key repeat so backspace can be held down to trigger love.keypressed multiple times.
  love.keyboard.setKeyRepeat(true)
  frogs = love.audio.newSource("Frogs_pitchshift.wav", "static")
  coin  = love.audio.newSource("coin.mp3", "static")

  love.window.setTitle( "Mixer" )
end

function love.keypressed(key, scancode, isrepeat)
  if key == "escape" then
    love.event.quit()

  -- elseif key == "s" and love.keyboard.isDown("lctrl") then
    -- saveHyperphoto()
-- 
  -- elseif key == "f11" then
    -- fullscreen = not fullscreen
    -- love.window.setFullscreen(fullscreen, "exclusive")
  end
end

function love.mousepressed(x, y, button, istouch)
  if button == 1 then
  	if x >= 20 and x <= 20+120 and y >= 50 and y <= 50+60 then
  		-- sound:setVolume(0.9) -- 90% of ordinary volume
        -- sound:setPitch(0.5) 
        -- coin:setLooping(true)
        coin:play()
  	end
  end
end

function love.draw()
  love.graphics.setColor(1, 0, 0)
  -- Draw a rectangle at 20,50 with a size of 60x120
  love.graphics.rectangle("fill", 20, 50, 120, 60)
  love.graphics.setColor(0, 1, 0)
  love.graphics.printf("coin", 25, 55, love.graphics.getWidth())
end
