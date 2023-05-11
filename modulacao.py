import numpy


SAMPLE_RATE = 10000
LOW_FREQUENCY = 1300
HIGHT_FREQUENCY = 1700


def create_signal(start, duration, frequency, sample_rate):
    x = numpy.linspace(start = start, stop = (start + duration), num = int(sample_rate * duration))
    y = numpy.sin(frequency * 2 * numpy.pi * x)
    return x, y


def calculate_frequency(signal):
    x, y = signal
    fourier = numpy.abs(numpy.fft.fft(y))
    frequencies = numpy.fft.fftfreq(x.size, (x[-1] - x[0]) / x.size)
    return numpy.abs(frequencies[numpy.argmax(fourier)])


def modulate(message):
    x = numpy.array([])
    y = numpy.array([])
    
    binary_message = bin(int.from_bytes(message.encode(), 'big')).replace('b', '')
    start = 0
    
    for bit in binary_message:
        signal_x, signal_y = create_signal(start = start, duration = 0.1, frequency = LOW_FREQUENCY if bit == '1' else HIGHT_FREQUENCY, sample_rate = SAMPLE_RATE)
        x = numpy.concatenate((x, signal_x))
        y = numpy.concatenate((y, signal_y))
        start += 0.1

    return x, y


def demodulate(signal):
    x, y = signal
    binary_message = '0b'
    
    for (x_chunk, y_chunk) in zip(numpy.split(x, x.size // 1000), numpy.split(y, y.size // 1000)):
        frequency = round(calculate_frequency((x_chunk, y_chunk)))
        
        if frequency == LOW_FREQUENCY:
            binary_message += '1'
        elif frequency == HIGHT_FREQUENCY:
            binary_message += '0'

    n = int(binary_message, 2)
    message = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return message


message = 'hello comp'
print(f'Original message: {message}')

x, y = modulate(message)
decoded_message = demodulate((x, y))
print(f'Decoded message: {decoded_message}')

