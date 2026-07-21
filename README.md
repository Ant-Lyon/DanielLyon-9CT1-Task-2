# DanielLyon-9CT1-Task-2


local x = 10

local function printSomething(sentence)
    print(sentence)
end

if x > 5 then
    printSomething(67)
elseif x < 5 then
    print("Brandon has no friends!")
else
    print("Brandon has {x} friends") -- string interpolation
end

local x = function()