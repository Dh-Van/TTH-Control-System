# giga_config.py
# COMPLETE PWM MAP for Arduino Giga R1 (STM32H7)
# Format: 'PIN': (TIMER_ID, CHANNEL_ID)

SERVO_MAP = {
    # --- GROUP A: PRIMARY PINS (Standard Arduino Header) ---
    # These are the most reliable pins to use.
    'D2':  (2, 4),  # TIM2 CH4
    'D3':  (2, 3),  # TIM2 CH3
    'D4':  (8, 1),  # TIM8 CH1 (Advanced Timer)
    'D5':  (3, 2),  # TIM3 CH2
    'D6':  (4, 2),  # TIM4 CH2
    'D7':  (3, 1),  # TIM3 CH1
    'D8':  (4, 3),  # TIM4 CH3
    'D9':  (4, 4),  # TIM4 CH4
    'D10': (2, 2),  # TIM2 CH2
    'D11': (8, 2),  # TIM8 CH2 (Advanced Timer)
    'D13': (12, 1), # TIM12 CH1
    
    # --- GROUP B: HIGH DIGITAL PINS (D22 - D53) ---
    # Verified Safe. (Others like D38, D46, D49 are inverted/complementary and unsafe).
    'D37': (8, 2),  # TIM8 CH2  (WARNING: Shared with D11)
    'D40': (15, 2), # TIM15 CH2 
    'D51': (15, 1), # TIM15 CH1 

    # --- GROUP C: ANALOG PINS (Used as Digital PWM) ---
    'A2':  (5, 3),  # TIM5 CH3
    'A3':  (5, 4),  # TIM5 CH4
    'A7':  (2, 1),  # TIM2 CH1 (Pin PA0)
}

# --- EXCLUDED PINS (DO NOT USE) ---
# D1, D48, D52 -> Connected to Timer 1 (System Clock - Reserved)
# D12, D38, D46, D16 -> Connected to "N" channels (Complementary/Inverted)
# D49 -> Connected to TIM15_CH1N (Inverted)