#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: aci_bd
short_description: Manage Bridge Domains (BD) on Cisco ACI Fabrics (fv:BD)
description:
- Manages Bridge Domains (BD) on Cisco ACI Fabrics.
- More information from the internal APIC class
  I(fv:BD) at U(https://developer.cisco.com/media/mim-ref/MO-fvBD.html).
author:
- Swetha Chunduri (@schunduri)
- Dag Wieers (@dagwieers)
- Jacob McGill (@jmcgill298)
requirements:
- ACI Fabric 1.0(3f)+
version_added: '2.4'
notes:
- The C(tenant) used must exist before using this module in your playbook.
  The M(aci_tenant) module can be used for this.
options:
  arp_flooding:
    description:
    - Determines if the Bridge Domain should flood ARP traffic.
    - The APIC defaults new Bridge Domains to "no".
    choices: [ no, yes ]
  bd:
    description:
    - The name of the Bridge Domain.
    aliases: [ bd_name, name ]
  bd_type:
    description:
    - The type of traffic on the Bridge Domain.
    - The APIC defaults new Bridge Domains to Ethernet.
    choices: [ ethernet, fc ]
  description:
    description:
    - Description for the Bridge Domain.
  enable_multicast:
    description:
    - Determines if PIM is enabled
    - The APIC defaults new Bridge Domains to disabled.
    choices: [ no, yes ]
  enable_routing:
    description:
    - Determines if IP forwarding should be allowed.
    - The APIC defaults new Bridge Domains to IP forwarding enabled.
    choices: [ no, yes ]
  endpoint_clear:
    description:
    - Clears all End Points in all Leaves when enabled.
    - The APIC defaults new Bridge Domains to disabled.
    - The value is not reset to disabled once End Points have been cleared; that requires a second task.
    choices: [ no, yes ]
  endpoint_move_detect:
    description:
    - Determines if GARP should be enabled to detect when End Points move.
    - The APIC defaults new Bridge Domains to not use GARP.
    choices: [ default, garp ]
  endpoint_retention_action:
   description:
   - Determines if the Bridge Domain should inherit or resolve the End Point Retention Policy.
   - The APIC defaults new Bridge Domain to End Point Retention Policies to resolve the policy.
  endpoint_retention_policy:
    description:
    - The name of the End Point Retention Policy the Bridge Domain should use when
      overriding the default End Point Retention Policy.
    choices: [ inherit, resolve ]
  igmp_snoop_policy:
    description:
    - The name of the IGMP Snooping Policy the Bridge Domain should use when
      overriding the default IGMP Snooping Policy.
  ip_learning:
    description:
    - Determines if the Bridge Domain should learn End Point IPs.
    - The APIC defaults new Bridge Domains to enable IP learning.
    choices: [ no, yes ]
  ipv6_nd_policy:
    description:
    - The name of the IPv6 Neighbor Discovery Policy the Bridge Domain should use when
      overridding teh default IPV6 ND Policy.
  l2_unknown_unicast:
    description:
    - Determines what forwarding method to use for unknown l2 destinations.
    - The APIC defaults new Bridge domains to use Hardware Proxy.
    choices: [ proxy, flood ]
  l3_unknown_multicast:
    description:
    - Determines the forwarding method to use for unknown multicast destinations.
    - The APCI defaults new Bridge Domains to use normal flooding.
    choices: [ flood, opt-flood ]
  limit_ip_learn:
    description:
    - Determines if the BD should limit IP learning to only subnets owned by the Bridge Domain.
    - The APIC defaults new Bridge Domains to learn all IP addresses.
    choices: [ no, yes ]
  multi_dest:
    description:
    - Determines the forwarding method for L2 multicast, broadcast, and link layer traffic.
    - The APIC defaults new Bridge Domains to use bd-flood.
    choices: [ bd-flood, drop, encap-flood ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    choices: [ absent, present, query ]
    default: present
  tenant:
    description:
    - The name of the Tenant.
    aliases: [ tenant_name ]
  vrf:
    description:
    - The name of the VRF.
    aliases: [ vrf_name ]
'''

EXAMPLES = r'''
- name: Add Bridge Domain
  aci_bd:
    action: "{{ action }}"
    tenant: "{{ tenant }}"
    bd: "{{ bd }}"
    vrf: "{{ vrf }}"
    arp_flooding: "{{ arp_flooding }}"
    l2_unknown_unicast: "{{ l2_unknown_unicast }}"
    l3_unknown_multicast: "{{ l3_unknown_multicast }}"
    multi_dest: "{{ multi_dest }}"
    gateway_ip: "{{ gateway_ip }}"
    subnet_mask: "{{ subnet_mask }}"
    scope: "{{ scope }}"
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    protocol: "{{ protocol }}"
'''

RETURN = r''' # '''

from ansible.module_utils.aci import ACIModule, aci_argument_spec
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = aci_argument_spec
    argument_spec.update(
        arp_flooding=dict(choices=['no', 'yes']),
        bd=dict(type='str', aliases=['bd_name', 'name']),
        bd_type=dict(type='str', choices=['ethernet', 'fc']),
        description=dict(type='str'),
        enable_multicast=dict(type='str', choices=['no', 'yes']),
        enable_routing=dict(type='str', choices=['no', 'yes']),
        endpoint_clear=dict(type='str', choices=['no', 'yes']),
        endpoint_move_detect=dict(type='str', choices=['default', 'garp']),
        endpoint_retention_action=dict(type='str', choices=['inherit', 'resolve']),
        endpoint_retention_policy=dict(type='str'),
        igmp_snoop_policy=dict(type='str'),
        ip_learning=dict(type='str', choices=['no', 'yes']),
        ipv6_nd_policy=dict(type='str'),
        l2_unknown_unicast=dict(choices=['proxy', 'flood']),
        l3_unknown_multicast=dict(choices=['flood', 'opt-flood']),
        limit_ip_learn=dict(type='str', choices=['no', 'yes']),
        multi_dest=dict(choices=['bd-flood', 'drop', 'encap-flood']),
        state=dict(choices=['absent', 'present', 'query'], type='str', default='present'),
        tenant=dict(type='str', aliases=['tenant_name']),
        vrf=dict(type='str', aliases=['vrf_name']),
        gateway_ip=dict(type='str', removed_in_version='2.4'),  # Deprecated starting from v2.4
        method=dict(type='str', choices=['delete', 'get', 'post'], aliases=['action'], removed_in_version='2.6'),  # Deprecated starting from v2.6
        scope=dict(type='str', removed_in_version='2.4'),  # Deprecated starting from v2.4
        subnet_mask=dict(type='str', removed_in_version='2.4')  # Deprecated starting from v2.4
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[['state', 'absent', ['bd', 'tenant']],
                     ['state', 'present', ['bd', 'tenant']]]
    )

    l2_unknown_unicast = module.params['l2_unknown_unicast']
    l3_unknown_multicast = module.params['l3_unknown_multicast']
    arp_flooding = module.params['arp_flooding']
    bd = module.params['bd']
    bd_type = module.params['bd_type']
    if bd_type == 'ethernet':
        # ethernet type is represented as regular, but that is not clear to the users
        bd_type = 'regular'
    description = module.params['description']
    enable_multicast = module.params['enable_multicast']
    enable_routing = module.params['enable_routing']
    endpoint_clear = module.params['endpoint_clear']
    endpoint_move_detect = module.params['endpoint_move_detect']
    if endpoint_move_detect == 'default':
        # the ACI default setting is an empty string, but that is not a good input value
        endpoint_move_detect = ''
    endpoint_retention_action = module.params['endpoint_retention_action']
    endpoint_retention_policy = module.params['endpoint_retention_policy']
    igmp_snoop_policy = module.params['igmp_snoop_policy']
    ip_learning = module.params['ip_learning']
    ipv6_nd_policy = module.params['ipv6_nd_policy']
    limit_ip_learn = module.params['limit_ip_learn']
    multi_dest = module.params['multi_dest']
    state = module.params['state']
    tenant = module.params['tenant']
    vrf = module.params['vrf']

    # Give warning when fvSubnet parameters are passed as those have been moved to the aci_subnet module
    if module.params['gateway_ip'] or module.params['subnet_mask'] or module.params['scope']:
        module._warnings = ["The support for managing Subnets has been moved to its own module, aci_subnet. \
                            The new modules still supports 'gateway_ip' and 'subnet_mask' along with more features"]

    if bd is not None:
        if tenant is not None:
            path = 'api/mo/uni/tn-%(tenant)s/BD-%(bd)s.json' % module.params
            filter_string = '?rsp-subtree=full&rsp-subtree-class=fvRsCtx,fvRsIgmpsn,fvRsBDToNdP,fvRsBdToEpRet&rsp-prop-include=config-only'
        else:
            path = 'api/class/fvBD.json'
            filter_string = ('?query-target-filter=eq(fvBD.name, \"%(bd)s\")&rsp-subtree=children'
                             '&rsp-subtree-class=fvRsCtx,fvRsIgmpsn,fvRsBDToNdP,fvRsBdToEpRet') % module.params
    elif tenant is not None:
        path = 'api/mo/uni/tn-%(tenant)s.json' % module.params
        filter_string = '?rsp-subtree=full&rsp-subtree-class=fvBD,fvRsCtx,fvRsIgmpsn,fvRsBDToNdP,fvRsBdToEpRet'
    else:
        path = 'api/class/fvBD.json'
        filter_string = "?rsp-subtree=full&rsp-subtree-class=fvBD,fvRsCtx,fvRsIgmpsn,fvRsBDToNdP,fvRsBdToEpRet"

    aci = ACIModule(module)

    aci.result['url'] = '%(protocol)s://%(hostname)s/' % aci.params + path

    aci.get_existing(filter_string=filter_string)

    if state == 'present':
        # Filter out module params with null values
        aci.payload(aci_class='fvBD',
                    class_config=dict(arpFlood=arp_flooding,
                                      descr=description,
                                      epClear=endpoint_clear,
                                      epMoveDetectMode=endpoint_move_detect,
                                      ipLearning=ip_learning,
                                      limitIpLearnToSubnets=limit_ip_learn,
                                      mcastAllow=enable_multicast,
                                      multiDstPktAct=multi_dest,
                                      name=bd,
                                      type=bd_type,
                                      unicastRoute=enable_routing,
                                      unkMacUcastAct=l2_unknown_unicast,
                                      unkMcastAct=l3_unknown_multicast),
                    child_configs=[{'fvRsCtx': {'attributes': {'tnFvCtxName': vrf}}},
                                   {'fvRsIgmpsn': {'attributes': {'tnIgmpSnoopPolName': igmp_snoop_policy}}},
                                   {'fvRsBDToNdP': {'attributes': {'tnNdIfPolName': ipv6_nd_policy}}},
                                   {'fvRsBdToEpRet': {'attributes': {'resolveAct': endpoint_retention_action,
                                    'tnFvEpRetPolName': endpoint_retention_policy}}}]
                    )

        # generate config diff which will be used as POST request body
        aci.get_diff(aci_class='fvBD')

        # submit changes if module not in check_mode and the proposed is different than existing
        aci.post_config()

    elif state == 'absent':
        aci.delete_config()

    module.exit_json(**aci.result)


if __name__ == "__main__":
    main()
