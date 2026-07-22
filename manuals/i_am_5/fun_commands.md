# Chapter 3: Fun Commands -- Let's Play!

Now for the fun part! Here are all the cool things you can tell Advika to do.

---

## How to Talk to Advika

Advika understands **spoken commands**! Just say her name first:

> **"Advika, [your command here]"**

Speak clearly and not too fast. Advika is still learning!

---

## Driving Commands

| You Say | Advika Does |
|---------|-------------|
| "Advika, go forward!" | Drives straight ahead |
| "Advika, go backward!" | Reverses carefully |
| "Advika, turn left!" | Spins to the left |
| "Advika, turn right!" | Spins to the right |
| "Advika, spin around!" | Does a 360 degree dance |
| "Advika, stop!" | Stops immediately |

**Pro Tip:** You can say "Advika, go forward one meter" and she'll measure the distance!

---

## Finding Things

| You Say | Advika Does |
|---------|-------------|
| "Advika, find the red cone!" | Looks around and drives to the red cone |
| "Advika, where is my shoe?" | Scans the room for shoe-like objects |
| "Advika, find Mommy!" | Looks for a person and drives toward them |
| "Advika, find the ball!" | Finds round objects and stops nearby |

---

## Fun & Games

| You Say | Advika Does |
|---------|-------------|
| "Advika, say hello!" | Says "Hello!" in her robot voice |
| "Advika, tell me a joke!" | Tells a kid-friendly robot joke |
| "Advika, do a dance!" | Spins and wiggles (driving dance!) |
| "Advika, follow me!" | Follows you around the room |
| "Advika, hide and seek!" | Counts to 10, then tries to find you |
| "Advika, patrol mode!" | Walks around the room like a guard |

---

## Status Checks

| You Say | Advika Tells You |
|---------|-----------------|
| "Advika, how are you?" | Battery level and mood |
| "Advika, what do you see?" | Describes objects in view |
| "Advika, are you safe?" | Checks all sensors and reports |

---

## Creative Commands

| You Say | Advika Does |
|---------|-------------|
| "Advika, draw a square!" | Drives in a square pattern |
| "Advika, draw a circle!" | Drives in a circle |
| "Advika, figure eight!" | Drives a figure-8 pattern |
| "Advika, zig zag!" | Drives in a zig-zag pattern |

---

## Challenge Modes!

### Level 1: Easy
- "Advika, go to the blue tape line and stop."
- "Advika, turn around three times."

### Level 2: Medium
- "Advika, find the red cone, then find the blue cone."
- "Advika, drive around the table without touching it."

### Level 3: Hard
- "Advika, make a maze and solve it!"
- "Advika, deliver this toy to the couch."

### Level 4: Expert
- "Advika, map the whole room!"
- "Advika, remember where things are and don't bump them."

---

## Making Your Own Commands!

Want to teach Advika something new? Ask a grown-up to help you edit the code!

In `mcp_servers/hardware_bridge.py`, you can add new commands by writing new functions with `@mcp.tool()`.

**Example: Make Advika wiggle**
```python
@mcp.tool()
def mcp_wiggle_robot(duration_ms: int = 1000):
    """Make Advika wiggle back and forth!"""
    # Wiggle left
    mcp_esp32_drive(0.0, 0.5, 250)
    time.sleep(0.3)
    # Wiggle right
    mcp_esp32_drive(0.0, -0.5, 250)
    time.sleep(0.3)
    # Wiggle left again
    mcp_esp32_drive(0.0, 0.5, 250)
    return {"status": "wiggled", "fun_level": "maximum"}
```

---

## Daily Missions

Here are missions you can give Advika every day:

### Monday: Mail Delivery
Put a small toy "letter" on Advika. Tell her to deliver it to the couch!

### Tuesday: Room Patrol
Have Advika drive around the room and report what she sees.

### Wednesday: Obstacle Course
Set up pillows and boxes. Time how fast Advika can navigate through!

### Thursday: Follow the Leader
Walk around and see if Advika can follow you without bumping into things.

### Friday: Treasure Hunt
Hide a red cone. Give Advika clues to find it!

### Saturday: Dance Party
Play music and have Advika do her driving dance!

### Sunday: Rest Day
Let Advika sleep (charge her battery). Draw pictures of your adventures!

---

## Secret Codes

Try these special phrases:

- **"Advika, secret mode!"** -- She whispers her sensor readings
- **"Advika, robot language!"** -- She beeps instead of talking
- **"Advika, turbo mode!"** -- She goes a little faster (careful!)

---

*Remember: The more you play with Advika, the smarter she gets!*

*Every adventure teaches her something new!*
