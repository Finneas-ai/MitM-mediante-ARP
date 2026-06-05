# 🕵️ MitM mediante ARP (ARP Spoofing)

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Scapy](https://img.shields.io/badge/Scapy-required-orange)](https://scapy.net/)
[![License](https://img.shields.io/badge/License-Educational-green)]()
[![Video Demo](https://img.shields.io/badge/Demo-YouTube-red?logo=youtube)](https://youtu.be/OZfx63OOdUs)

---

## 🎬 Demo

📺 [Ver video de demostración](https://youtu.be/OZfx63OOdUs)

---

## 📋 Descripción

Este laboratorio demuestra cómo un atacante puede interceptar la comunicación entre una estación de trabajo y su gateway predeterminado mediante la técnica de **envenenamiento de tablas ARP (ARP Spoofing)**.

Se busca comprender el funcionamiento de los ataques **Man-in-the-Middle (MitM)**, observando cómo la manipulación de las asociaciones entre direcciones IP y direcciones MAC permite que el tráfico de red pase por el equipo atacante antes de llegar a su destino.

---

## 🎯 Objetivos

### Objetivo del Laboratorio
Demostrar cómo un atacante intercepta comunicación mediante envenenamiento ARP, analizando los riesgos sobre la **confidencialidad**, **integridad** y **disponibilidad** de la información transmitida en una red local.

### Objetivo del Script
Enviar de manera continua respuestas ARP falsificadas tanto a la máquina víctima como al gateway, alterando sus tablas ARP para que asocien las IPs legítimas con la MAC del atacante, redirigiendo así todo el tráfico.

---

## ⚙️ Requisitos

- Python 3.x
- Scapy (`pip install scapy`)
- Permisos root
- IP Forwarding habilitado:
  ```bash
  echo 1 > /proc/sys/net/ipv4/ip_forward
  ```

---

## 🚀 Uso

```bash
sudo python3 MITM.py <iface> -v <victim_ip> [-i <interval>]
```

### Parámetros

| Parámetro | Descripción | Obligatorio |
|-----------|-------------|:-----------:|
| `iface` | Interfaz de red del atacante (ej. `eth0`) | ✅ |
| `-v` / `--victim` | IP de la víctima | ✅ |
| `-i` / `--interval` | Intervalo de reenvío ARP en segundos | ❌ |

### Ejemplo

```bash
sudo python3 MITM.py ens3 -v 10.6.82.22 -i 2
```

---

## 🔄 Flujo de Ejecución

```
1. Resolución de MACs reales de víctima y gateway via ARP
2. Envío de ARP replies falsos a la víctima → MAC gateway = MAC atacante
3. Envío de ARP replies falsos al gateway → MAC víctima = MAC atacante
4. Con IP forwarding activo, el atacante retransmite el tráfico (intercepción transparente)
5. Al interrumpir (Ctrl+C), se restauran las tablas ARP con los valores reales
```

---

## 🛡️ Contramedidas

| Medida | Comando / Acción | Efecto |
|--------|-----------------|--------|
| ARP estático en hosts críticos | `arp -s <ip> <mac>` | Impide sobrescritura de entradas críticas |

---


## ⚠️ Aviso Legal

> Este proyecto es exclusivamente con fines **educativos** en un entorno controlado de laboratorio. El uso de estas técnicas fuera de entornos autorizados es ilegal y éticamente incorrecto.
