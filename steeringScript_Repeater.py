from panda import Panda


def can_modify(dat):
    lkaData = dat[0:4]

    # pulls values out of lkaData
    rollingCounter = lkaData[0]>>4 & 0b11
    active = lkaData[0]>>3 & 0b1
    steerCommand = (lkaData[0] & 0b111) << 8 | lkaData[1]

    # modify values here
    active = 1
    steerCommand = 150

    newChecksum = 0x1000 - (active << 11) - (steerCommand & 0x7ff) - rollingCounter
    dat[0] = (lkaData[0] & 0b11000000) | (rollingCounter << 4) | (active << 3) | (steerCommand >> 8)
    dat[1] = (steerCommand & 0b11111111)
    dat[2] = (lkaData[2] & 0b11110000) | (newChecksum >> 8)
    dat[3] = (newChecksum & 0b11111111)

    return dat

def can_proxy():
  print("Trying to connect to Panda over USB...")
  p = Panda()
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  p.can_clear(0)

  try:
    while True:
      can_recv = p.can_recv()
      for address, _, dat, src  in can_recv:
        if src == 2:
          if address == 0x180:
            dat = can_modify(dat)
            p.can_send(address, bytearray(dat), 0)
            print("sent message")


  except KeyboardInterrupt:
    print("\nNow exiting.")


can_proxy()