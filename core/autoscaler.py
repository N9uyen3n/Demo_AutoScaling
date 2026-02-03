import math
from typing import Tuple
import config

class Autoscaler:
    def __init__(self, min_servers=config.MIN_REPLICAS, max_servers=config.MAX_REPLICAS):
        self.cooldown_counter = 0
        self.last_action = "NONE"
        self.min_servers = min_servers
        self.max_servers = max_servers
        self.capacity_per_replica = config.DEFAULT_SCALE_OUT_THRESHOLD

    def calculate_replicas(self, current_load: float, forecast_load: float, current_replicas: int) -> Tuple[int, str, float]:
        """
        Calculates required replicas using 3-Layer Defense Strategy.
        current_replicas: Needed for Rule-based layer (Cooldown).
        
        Returns: (num_replicas, reason, estimated_cost)
        """
        reason = []
        
        # ─────────────────────────────────────────────────────────────
        # LAYER 1: PREDICTIVE (Attack) - Proactive Scaling
        # ─────────────────────────────────────────────────────────────
        # Convert Forecast Load -> Replicas
        predictive_target = math.ceil(forecast_load / self.capacity_per_replica)
        reason.append(f"Pred:{predictive_target}")

        # ─────────────────────────────────────────────────────────────
        # LAYER 2: REACTIVE (Defense) - Safety Net
        # ─────────────────────────────────────────────────────────────
        # Convert Current Real Load -> Replicas
        reactive_target = math.ceil(current_load / self.capacity_per_replica)
        
        # Logic: If Reactive > Predictive, it means the model is underestimating (DANGER).
        # We must override immediately to prevent crash.
        if reactive_target > predictive_target:
            target_replicas = reactive_target
            reason.append(f"React:{reactive_target} (Override)")
        else:
            target_replicas = predictive_target
            # Predictive is higher (Pre-warming) or equal. Safe to follow forecast.
        
        # ─────────────────────────────────────────────────────────────
        # LAYER 3: RULE-BASED (Stability) - Cooldown & Bounds
        # ─────────────────────────────────────────────────────────────
        # Apply Bounds First
        target_replicas = max(target_replicas, self.min_servers)
        target_replicas = min(target_replicas, self.max_servers)
        
        action = "STABLE"
        
        if target_replicas > current_replicas:
            # SCALE OUT: "Fast"
            # Rule: Always allow Scale Out to capture traffic spikes.
            # Reset cooldown to prevent immediate flapping after this scale out.
            self.cooldown_counter = config.DEFAULT_COOLDOWN_PERIOD 
            action = "SCALE OUT"
            
        elif target_replicas < current_replicas:
            # SCALE IN: "Slow"
            # Rule: Only allow Scale In if cooldown is expired.
            if self.cooldown_counter > 0:
                # BLOCKED by Layer 3
                target_replicas = current_replicas # Keep current state
                self.cooldown_counter -= 1
                reason.append(f"Cooldown:{self.cooldown_counter}")
                action = "COOLDOWN"
            else:
                # Allowed
                self.cooldown_counter = config.DEFAULT_COOLDOWN_PERIOD
                action = "SCALE IN"
        
        else:
            # Stable
            if self.cooldown_counter > 0:
                self.cooldown_counter -= 1
        
        final_reason = f"[{action}] " + " | ".join(reason)
        cost = target_replicas * config.COST_PER_REPLICA_PER_TICK
        
        details = {
            "predictive_target": predictive_target,
            "reactive_target": reactive_target,
            "final_target": target_replicas,
            "action": action,
            "cooldown": self.cooldown_counter,
            "layer_msg": reason
        }
        
        return target_replicas, final_reason, cost, details
