package p2s

import (
	"errors"
)

type Cmc struct {
	Head       Header
	Chan1      uint32
	Chan2      uint32
	PeerID     string
	IsOnline   uint8
	MaxSuppose uint32
	CurSuppose uint32
}

func NewCmc() *Cmc {
	p := new(Cmc)
	return p
}

func (p *Cmc) Decode(data []byte) error {
	return nil
}

func (p *Cmc) Encode() ([]byte, error) {
	data := NewBuffer(maxBufferSize)

	//version
	err := data.PutUint32(littleFlag, uint32(p.Head.Ver))
	if err != nil {
		return nil, errors.New("Cmc:put version error")
	}

	//command type
	err = data.PutUint8(p.Head.CmdId)
	if err != nil {
		return nil, errors.New("Cmc:put command type error")
	}

	err = data.PutUint32(littleFlag, p.Chan1)
	if err != nil {
		return nil, errors.New("Cmc:put nat type error")
	}

	err = data.PutUint32(littleFlag, p.Chan2)
	if err != nil {
		return nil, errors.New("Cmc:put nat type error")
	}

	//local peerid len
	localPeerIDLen := len(p.PeerID)
	err = data.PutUint32(littleFlag, uint32(localPeerIDLen))
	if err != nil {
		return nil, errors.New("Cmc:put local peerid len error")
	}

	//local peerid
	err = data.PutString(localPeerIDLen, p.PeerID)
	if err != nil {
		return nil, errors.New("Cmc:put local peerid error")
	}

	//remote peer fuzzy typr
	err = data.PutUint8(p.IsOnline)
	if err != nil {
		return nil, errors.New("Cmc:put remote peer fuzzy type error")
	}

	err = data.PutUint32(littleFlag, p.MaxSuppose)
	if err != nil {
		return nil, errors.New("Cmc:put nat type error")
	}

	err = data.PutUint32(littleFlag, p.CurSuppose)
	if err != nil {
		return nil, errors.New("Cmc:put nat type error")
	}

	return data.buf[data.limit:data.pos], nil
}
