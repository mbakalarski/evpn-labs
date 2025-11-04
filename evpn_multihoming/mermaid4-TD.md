```mermaid
graph TD
    %% Auto-generated GitHub-compatible network topology diagram

    classDef srlinux fill:#b3d9ff,stroke:#003366,stroke-width:2px;
    classDef linux fill:#b3ffb3,stroke:#006600,stroke-width:2px;
    classDef network fill:#fff5b3,stroke:#b38f00,stroke-width:1px,shape:circle;

    subgraph Spine_Leaf_Networks
        spine1 --> s1
        leaf1 --> s1
        spine1 --> s2
        leaf2 --> s2
        spine1 --> s3
        leaf3 --> s3
    end

    subgraph Leaf_CE_Networks
        leaf1 --> l1
        ce1 --> l1
        leaf2 --> l2
        ce1 --> l2
        leaf3 --> l3
        ce2 --> l3
        leaf3 --> l4
        ce2 --> l4
        leaf3 --> l5
        ce2 --> l5
    end

    %% Assign node styles
    class spine1 srlinux;
    class leaf1 srlinux;
    class leaf2 srlinux;
    class leaf3 srlinux;
    class ce1 linux;
    class ce2 linux;
    class s1 network;
    class s2 network;
    class s3 network;
    class l1 network;
    class l2 network;
    class l3 network;
    class l4 network;
    class l5 network;
```
