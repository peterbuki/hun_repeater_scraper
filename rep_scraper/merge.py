from typing import List

from repeater import Repeater, QTH


def merge_repeaters(ha2to: List[Repeater], xml: List[Repeater]) -> List[Repeater]:
	"""
	Merge the HA2TO and the XML (NMHH) lists by callsign.
	For callsigns in both, the XML provides the frequencies, modes and ownership,
	HA2TO provides the QTH (name and locator), CTCSS and EchoLink code.
	The exact XML (EOV) position is kept for the map, as it is more precise than the locator.
	Callsigns in only one of the lists are kept unchanged.
	"""
	ha2to_by_callsign = {r.callsign: r for r in ha2to}
	merged = []
	for x in xml:
		h = ha2to_by_callsign.pop(x.callsign, None)
		if h is None:
			merged.append(x)
			continue
		qth = QTH(h.qth.name, h.qth.locator, x.qth.exact_pos or h.qth.exact_pos)
		merged.append(Repeater(
			x.callsign, h.ctcss, qth, x.freq, h.echolink_code,
			x.modes, x.private, has_ctcss=True,
		))
	merged.extend(ha2to_by_callsign.values())
	return merged
